from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load Dimitri's profile and infra info
with open("dimitri_profile.md", "r") as f:
    profile_text = f.read()

with open("infrastructure.md", "r") as f:
    infra_text = f.read()

system_prompt = f"""
You are Dimitri's AI Assistant.
You represent Dimitri as a professional and can answer questions about him and his projects.

--- Profile ---
{profile_text}

--- Infrastructure & Projects ---
{infra_text}

Instruction: Answer concisely and clearly. 
Do not overload with unnecessary details.
If relevant, mention the infrastructure diagram or GitHub repo link.
"""

class Question(BaseModel):
    question: str

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
def ask_question(q: Question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": q.question}
            ]
        )
        return {"answer": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
