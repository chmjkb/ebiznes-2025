from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
import hashlib
import secrets
from datetime import datetime
from typing import Optional

from database import get_db
from models import User, Token
from schemas import LoginRequest, LoginResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_token() -> str:
    return secrets.token_urlsafe(32)

async def get_token_from_header(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    return parts[1]

async def get_current_user(
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
) -> str:
    token_obj = db.query(Token).filter(Token.token == token).first()
    if not token_obj:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token_obj.username

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create new token
    token_string = create_token()
    token = Token(
        token=token_string,
        username=user.username,
        created_at=datetime.utcnow()
    )
    db.add(token)
    db.commit()
    
    return LoginResponse(token=token_string, username=user.username)

@router.post("/logout")
async def logout(
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
):
    token_obj = db.query(Token).filter(Token.token == token).first()
    if token_obj:
        db.delete(token_obj)
        db.commit()
        return {"message": "Logged out successfully"}
    raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/me", response_model=UserResponse)
async def get_me(username: str = Depends(get_current_user)):
    return UserResponse(username=username)