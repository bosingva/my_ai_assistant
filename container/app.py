# container/app.py - UPDATED VERSION with conversation tracking

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
import os
import boto3
from datetime import datetime
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# AWS Clients
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
ses_client = boto3.client('ses', region_name=os.getenv('AWS_REGION', 'us-east-1'))

# DynamoDB table name (will create via Terraform)
CONVERSATIONS_TABLE = os.getenv('CONVERSATIONS_TABLE', 'ai-assistant-conversations')

# Load all documents
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

def log_conversation(visitor_ip: str, user_agent: str, question: str, answer: str):
    """
    Log conversation to DynamoDB
    """
    try:
        table = dynamodb.Table(CONVERSATIONS_TABLE)
        conversation_id = f"{visitor_ip}_{datetime.utcnow().isoformat()}"
        
        table.put_item(
            Item={
                'conversation_id': conversation_id,
                'timestamp': datetime.utcnow().isoformat(),
                'visitor_ip': visitor_ip,
                'user_agent': user_agent,
                'question': question,
                'answer': answer,
                'ttl': int(datetime.utcnow().timestamp()) + (90 * 24 * 60 * 60)  # 90 days retention
            }
        )
        return conversation_id
    except Exception as e:
        print(f"Error logging to DynamoDB: {str(e)}")
        return None

def send_email_notification(conversation_id: str, visitor_ip: str, question: str, answer: str):
    """
    Send email notification via AWS SES
    """
    try:
        email_body = f"""
New conversation with your AI Assistant!

Conversation ID: {conversation_id}
Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
Visitor IP: {visitor_ip}

Question:
{question}

Answer:
{answer}

---
View all conversations in DynamoDB table: {CONVERSATIONS_TABLE}
"""
        
        response = ses_client.send_email(
            Source='noreply@talk-to-my-ai.click',  # Must be verified in SES
            Destination={
                'ToAddresses': ['korgalidzed@gmail.com']
            },
            Message={
                'Subject': {
                    'Data': f'AI Assistant: New Conversation from {visitor_ip}',
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
def ask_question(q: Question, request: Request):
    try:
        # Get visitor information
        visitor_ip = request.client.host
        user_agent = request.headers.get('user-agent', 'Unknown')
        
        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": q.question}
            ]
        )
        
        answer = response.choices[0].message.content
        
        # Log to DynamoDB
        conversation_id = log_conversation(visitor_ip, user_agent, q.question, answer)
        
        # Send email notification
        if conversation_id:
            send_email_notification(conversation_id, visitor_ip, q.question, answer)
        
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health_check():
    """Health check endpoint for ALB"""
    return {"status": "healthy"}

@app.get("/conversations")
def get_recent_conversations():
    """
    API endpoint to view recent conversations (optional - for your dashboard)
    Protected by IP or add authentication
    """
    try:
        table = dynamodb.Table(CONVERSATIONS_TABLE)
        response = table.scan(Limit=50)
        items = response.get('Items', [])
        
        # Sort by timestamp
        items.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return {"conversations": items[:10]}  # Return last 10
    except Exception as e:
        return {"error": str(e)}
