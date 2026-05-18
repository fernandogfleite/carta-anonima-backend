from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.guess import Guess
from src.models.letter import Letter
from src.core.exceptions.app_exceptions import (
    NotFoundError,
    ValidationError,
)
from src.utils.normalization import normalize_name


class GuessesService:
    async def create(
        self, session: AsyncSession, letter_id: int, guessed_name: str
    ) -> Guess:
        result = await session.execute(
            select(Letter).where(Letter.id == letter_id).with_for_update()
        )
        letter = result.scalar_one_or_none()
        if not letter:
            raise NotFoundError("letter_not_found", "Carta nao encontrada")
        if letter.is_solved:
            raise ValidationError("letter_solved", "Carta ja resolvida")

        guessed_normalized = normalize_name(guessed_name)
        if not guessed_normalized:
            raise ValidationError("invalid_guess", "Nome de tentativa invalido")
        is_correct = guessed_normalized == letter.sender_name_normalized

        guess = Guess(
            letter_id=letter_id,
            guessed_name=guessed_name,
            guessed_name_normalized=guessed_normalized,
            is_correct=is_correct,
        )
        session.add(guess)
        if is_correct:
            letter.is_solved = True
            letter.solved_at = datetime.utcnow()
            letter.is_revealed = True
        await session.commit()
        await session.refresh(guess)
        attempts_count = (
            await session.execute(
                select(func.count(Guess.id)).where(Guess.letter_id == letter_id)
            )
        ).scalar_one()
        guess.attempts_count = attempts_count
        guess.letter_is_solved = letter.is_solved
        return guess

    async def stats(self, session: AsyncSession) -> dict:
        total_attempts = (
            await session.execute(select(func.count(Guess.id)))
        ).scalar_one()
        correct_attempts = (
            await session.execute(
                select(func.count(Guess.id)).where(Guess.is_correct.is_(True))
            )
        ).scalar_one()
        wrong_attempts = total_attempts - correct_attempts
        solved_letters = (
            await session.execute(
                select(func.count(Letter.id)).where(Letter.is_solved.is_(True))
            )
        ).scalar_one()
        total_letters = (
            await session.execute(select(func.count(Letter.id)))
        ).scalar_one()
        pending_letters = total_letters - solved_letters

        per_letter = (
            select(Guess.letter_id, func.count(Guess.id).label("attempts"))
            .join(Letter, Letter.id == Guess.letter_id)
            .where(Letter.is_solved.is_(True))
            .group_by(Guess.letter_id)
        ).subquery()
        attempts_per_solved = (
            await session.execute(select(func.avg(per_letter.c.attempts)))
        ).scalar_one_or_none()

        return {
            "total_attempts": total_attempts,
            "correct_attempts": correct_attempts,
            "wrong_attempts": wrong_attempts,
            "solved_letters": solved_letters,
            "pending_letters": pending_letters,
            "avg_attempts_to_solve": (
                float(attempts_per_solved) if attempts_per_solved is not None else None
            ),
        }
