from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
from typing import Optional, List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
logger.info(f"GROQ_API_KEY present: {bool(api_key)}")
logger.info(f"API Key length: {len(api_key) if api_key else 0}")

groq_client = Groq(
    api_key=api_key
)

class Message(BaseModel):
    role: str
    content: str

class PromptRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = "llama3-8b-8192"  # Updated to a supported model
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1024

class PromptResponse(BaseModel):
    response: str
    model: str
    usage: dict

@app.get("/")
async def health_check():
    return {"status": "healthy", "api_key_configured": bool(os.getenv("GROQ_API_KEY"))}

@app.post("/api/chat_completion", response_model=PromptResponse)
async def process_prompt(request: PromptRequest):
    logger.info(f"Received request with {len(request.messages)} messages, model={request.model}")
    
    try:
        logger.info("Calling Groq API...")
        # Convert Pydantic models to dict format for Groq API
        messages_dict = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        chat_completion = groq_client.chat.completions.create(
            messages=messages_dict,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        response_content = chat_completion.choices[0].message.content
        logger.info(f"Groq API response received, length: {len(response_content)}")
        
        return PromptResponse(
            response=response_content,
            model=request.model,
            usage=dict(chat_completion.usage)
        )
    
    except Exception as e:
        logger.error(f"Error in process_prompt: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
