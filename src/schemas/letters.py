from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class LetterCreate(BaseModel):
    content: str = Field(min_length=10, max_length=4000)
    sender_name: str = Field(min_length=2, max_length=120)
    anonymous_hint: str | None = Field(default=None, max_length=200)


class LetterUpdate(BaseModel):
    content: str | None = Field(default=None, min_length=10, max_length=4000)
    anonymous_hint: str | None = Field(default=None, max_length=200)
    is_revealed: bool | None = None
    is_solved: bool | None = None


class LetterRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    content: str
    anonymous_hint: str | None = None
    is_revealed: bool
    is_solved: bool
    solved_at: datetime | None = None
    attempts_count: int = 0
    created_at: datetime
    sender_name: str | None = None


class AdminLetterRead(LetterRead):
    model_config = ConfigDict(from_attributes=True)
    sender_name: str
