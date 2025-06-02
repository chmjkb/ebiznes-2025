from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User
import hashlib

SQLALCHEMY_DATABASE_URL = "sqlite:///./auth.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Create default users
    db = SessionLocal()
    try:
        # Check if users already exist
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                username="admin",
                password_hash=hashlib.sha256("admin123".encode()).hexdigest()
            )
            db.add(admin)
        
        if not db.query(User).filter(User.username == "user").first():
            user = User(
                username="user",
                password_hash=hashlib.sha256("user123".encode()).hexdigest()
            )
            db.add(user)
        
        db.commit()
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()