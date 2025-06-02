from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, pattern="^[a-zA-Z0-9]+$")
    password: str = Field(min_length=6)

class LoginResponse(BaseModel):
    token: str
    username: str

class UserResponse(BaseModel):
    username: str