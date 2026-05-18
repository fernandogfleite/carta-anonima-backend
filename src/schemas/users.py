from pydantic import BaseModel, ConfigDict

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    is_admin: bool

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
