from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    username = Column(String, primary_key=True, index=True)
    password_hash = Column(String, nullable=False)
    oauth_provider = Column(String, nullable=True)
    
    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")

class Token(Base):
    __tablename__ = "tokens"
    
    token = Column(String, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="tokens")