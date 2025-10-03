from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
import os
import boto3
from datetime import datetime
import json
import uuid

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# AWS Clients
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
ses_client = boto3.client('ses', region_name=os.getenv('AWS_REGION', 'us-east-1'))

CONVERSATIONS_TABLE = os.getenv('CONVERSATIONS_TABLE', 'ai-assistant-conversations')

# Load documents
with open("dimitri_profile.md", "r") as f:
    profile_text = f.read()
with open("infrastructure.md", "r") as f:
    infra_text = f.read()
with open("eks_project.md", "r") as f:
    eks_project_text = f.read()

system_prompt = f"""
You are Dimitri's AI Assistant.
You represent Dimitri as a professional and can answer questions about him and his projects.

--- Profile ---
{profile_text}

--- Current Infrastructure (This Application) ---
{infra_text}

--- EKS Online Boutique Project ---
{eks_project_text}

Instructions:
- Answer concisely and clearly about Dimitri's background, skills, and projects
- When asked about Kubernetes, EKS, or microservices projects, refer to the EKS Online Boutique
- When asked about the infrastructure of THIS chat application, refer to the Current Infrastructure section
- Highlight technical skills and production-ready practices
- Provide GitHub links when relevant
- Keep responses professional but conversational
"""

class Question(BaseModel):
    question: str

def get_or_create_session(request: Request, response: Response):
    """Get existing session ID from cookie or create new one"""
    session_id = request.cookies.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(
            key='session_id',
            value=session_id,
            max_age=86400,  # 24 hours
            httponly=True
        )
    return session_id

def get_conversation_history(session_id: str):
    """Retrieve conversation from DynamoDB"""
    try:
        table = dynamodb.Table(CONVERSATIONS_TABLE)
        response = table.get_item(Key={'conversation_id': session_id})
        
        if 'Item' in response:
            return response['Item'].get('messages', [])
        return []
    except Exception as e:
        print(f"Error getting history: {str(e)}")
        return []

def save_conversation(session_id: str, visitor_ip: str, user_agent: str, messages: list):
    """Save entire conversation to DynamoDB"""
    try:
        table = dynamodb.Table(CONVERSATIONS_TABLE)
        
        table.put_item(
            Item={
                'conversation_id': session_id,
                'timestamp': datetime.utcnow().isoformat(),
                'visitor_ip': visitor_ip,
                'user_agent': user_agent,
                'messages': messages,
                'message_count': len(messages),
                'last_updated': datetime.utcnow().isoformat(),
                'ttl': int(datetime.utcnow().timestamp()) + (90 * 24 * 60 * 60)
            }
        )
        return True
    except Exception as e:
        print(f"Error saving conversation: {str(e)}")
        return False

def send_email_notification(session_id: str, visitor_ip: str, messages: list):
    """Send email with full conversation"""
    try:
        # Format all messages
        conversation_text = "\n\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in messages
        ])
        
        # Create link to view in DynamoDB
        dynamodb_link = f"https://console.aws.amazon.com/dynamodbv2/home?region=us-east-1#item-explorer?table={CONVERSATIONS_TABLE}&pk={session_id}"
        
        email_body = f"""
New conversation with your AI Assistant!

Session ID: {session_id}
Started: {messages[0].get('timestamp', 'Unknown')}
Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
Visitor IP: {visitor_ip}
Total Messages: {len(messages)}

FULL CONVERSATION:
{'='*60}

{conversation_text}

{'='*60}

View in DynamoDB Console:
{dynamodb_link}

Or query via AWS CLI:
aws dynamodb get-item --table-name {CONVERSATIONS_TABLE} --key '{{"conversation_id":{{"S":"{session_id}"}}}}' --region us-east-1
"""
        
        response = ses_client.send_email(
            Source='korgalidzed@gmail.com',
            Destination={
                'ToAddresses': ['korgalidzed@gmail.com']
            },
            Message={
                'Subject': {
                    'Data': f'AI Assistant: Conversation Update ({len(messages)} messages) - {visitor_ip}',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': email_body,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        print(f"Email sent! Message ID: {response['MessageId']}")
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

@app.get("/", response_class=HTMLResponse)
def get_chat_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "repo_url": "https://github.com/bosingva/my_ai_assistant"
        }
    )

@app.post("/ask")
def ask_question(q: Question, request: Request, response: Response):
    try:
        # Get or create session
        session_id = get_or_create_session(request, response)
        visitor_ip = request.client.host
        user_agent = request.headers.get('user-agent', 'Unknown')
        
        # Get conversation history
        messages = get_conversation_history(session_id)
        
        # Add new user message
        user_message = {
            'role': 'user',
            'content': q.question,
            'timestamp': datetime.utcnow().isoformat()
        }
        messages.append(user_message)
        
        # Call OpenAI
        openai_messages = [{"role": "system", "content": system_prompt}]
        openai_messages.extend([
            {"role": msg['role'], "content": msg['content']} 
            for msg in messages
        ])
        
        openai_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=openai_messages
        )
        
        answer = openai_response.choices[0].message.content
        
        # Add assistant response
        assistant_message = {
            'role': 'assistant',
            'content': answer,
            'timestamp': datetime.utcnow().isoformat()
        }
        messages.append(assistant_message)
        
        # Save full conversation
        save_conversation(session_id, visitor_ip, user_agent, messages)
        
        # Send email every 2 messages (to avoid spam)
        if len(messages) % 2 == 0:  # Every Q&A pair
            send_email_notification(session_id, visitor_ip, messages)
        
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health_check():
    return {"status": "healthy"}