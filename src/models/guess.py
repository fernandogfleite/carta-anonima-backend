from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base


class Guess(Base):
    __tablename__ = "guesses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    letter_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("letters.id"), nullable=False
    )
    guessed_name: Mapped[str] = mapped_column(String, nullable=False)
    guessed_name_normalized: Mapped[str] = mapped_column(String, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    letter = relationship("Letter", back_populates="guesses")
