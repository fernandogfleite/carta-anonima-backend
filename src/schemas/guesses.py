from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class GuessCreate(BaseModel):
    letter_id: int
    guessed_name: str = Field(min_length=2, max_length=120)


class GuessRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    letter_id: int
    guessed_name: str
    is_correct: bool
    letter_is_solved: bool = False
    attempts_count: int = 0
    created_at: datetime


class GuessStats(BaseModel):
    total_attempts: int
    correct_attempts: int
    wrong_attempts: int
    solved_letters: int
    pending_letters: int
    avg_attempts_to_solve: float | None = None
