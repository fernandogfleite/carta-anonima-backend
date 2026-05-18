from pydantic import BaseModel, Field

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=128)
