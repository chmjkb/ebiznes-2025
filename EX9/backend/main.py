from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

class PromptRequest(BaseModel):
    prompt: str
    model: Optional[str] = "mixtral-8x7b-32768"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1024

class PromptResponse(BaseModel):
    response: str
    model: str
    usage: dict

@app.post("/api/chat_completion", response_model=PromptResponse)
async def process_prompt(request: PromptRequest):
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": request.prompt
                }
            ],
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        response_content = chat_completion.choices[0].message.content
        
        return PromptResponse(
            response=response_content,
            model=request.model,
            usage=dict(chat_completion.usage)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
