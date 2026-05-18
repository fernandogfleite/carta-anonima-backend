from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base


class Letter(Base):
    __tablename__ = "letters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    sender_name: Mapped[str] = mapped_column(String, nullable=False)
    sender_name_normalized: Mapped[str] = mapped_column(String, nullable=False)
    anonymous_hint: Mapped[str | None] = mapped_column(String, nullable=True)
    sender_ip: Mapped[str] = mapped_column(String, nullable=False)
    is_revealed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_solved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    solved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    guesses = relationship("Guess", back_populates="letter")
