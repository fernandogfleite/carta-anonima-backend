from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.letter import Letter
from src.models.guess import Guess


class AdminService:
    async def letters_summary(self, session: AsyncSession) -> dict:
        total_letters = (
            await session.execute(select(func.count(Letter.id)))
        ).scalar_one()
        revealed_letters = (
            await session.execute(
                select(func.count(Letter.id)).where(Letter.is_revealed.is_(True))
            )
        ).scalar_one()
        solved_letters = (
            await session.execute(
                select(func.count(Letter.id)).where(Letter.is_solved.is_(True))
            )
        ).scalar_one()
        pending_letters = total_letters - solved_letters
        total_guesses = (
            await session.execute(select(func.count(Guess.id)))
        ).scalar_one()
        return {
            "total_letters": total_letters,
            "revealed_letters": revealed_letters,
            "solved_letters": solved_letters,
            "pending_letters": pending_letters,
            "total_guesses": total_guesses,
        }
