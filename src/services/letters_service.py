from datetime import datetime, timedelta
from sqlalchemy import select, func, delete
from src.models.guess import Guess
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.letter import Letter
from src.core.exceptions.app_exceptions import (
    NotFoundError,
    ValidationError,
    RateLimitError,
)
from src.utils.normalization import normalize_name
from src.core.config.settings import get_settings


class LettersService:
    async def create(
        self,
        session: AsyncSession,
        content: str,
        sender_name: str,
        anonymous_hint: str | None,
        sender_ip: str,
    ) -> Letter:
        settings = get_settings()
        since = datetime.utcnow() - timedelta(seconds=settings.spam_window_seconds)
        spam_query = select(func.count(Letter.id)).where(
            Letter.sender_ip == sender_ip, Letter.created_at >= since
        )
        spam_count = (await session.execute(spam_query)).scalar_one()
        if spam_count >= settings.spam_max_attempts:
            raise RateLimitError("spam_limit", "Muitas cartas enviadas em pouco tempo")

        if not content.strip():
            raise ValidationError("invalid_content", "Conteudo da carta invalido")

        sender_name_normalized = normalize_name(sender_name)
        if not sender_name_normalized:
            raise ValidationError("invalid_sender_name", "Nome do remetente invalido")

        letter = Letter(
            content=content,
            sender_name=sender_name,
            sender_name_normalized=sender_name_normalized,
            anonymous_hint=anonymous_hint,
            sender_ip=sender_ip,
        )
        session.add(letter)
        await session.commit()
        await session.refresh(letter)
        return letter

    async def list(self, session: AsyncSession) -> list[Letter]:
        stmt = select(Letter).order_by(Letter.created_at.desc())
        result = await session.execute(stmt)
        letters = list(result.scalars().all())
        if not letters:
            return letters
        letter_ids = [letter.id for letter in letters]
        counts = (
            await session.execute(
                select(Guess.letter_id, func.count(Guess.id))
                .where(Guess.letter_id.in_(letter_ids))
                .group_by(Guess.letter_id)
            )
        ).all()
        count_map = {letter_id: count for letter_id, count in counts}
        for letter in letters:
            letter.attempts_count = count_map.get(letter.id, 0)
        return letters

    async def get(self, session: AsyncSession, letter_id: int) -> Letter:
        result = await session.execute(select(Letter).where(Letter.id == letter_id))
        letter = result.scalar_one_or_none()
        if not letter:
            raise NotFoundError("letter_not_found", "Carta nao encontrada")
        attempts_count = (
            await session.execute(
                select(func.count(Guess.id)).where(Guess.letter_id == letter_id)
            )
        ).scalar_one()
        letter.attempts_count = attempts_count
        return letter

    async def get_random(self, session: AsyncSession) -> Letter:
        stmt = select(Letter).order_by(func.random()).limit(1)
        result = await session.execute(stmt)
        letter = result.scalar_one_or_none()
        if not letter:
            raise NotFoundError("letter_not_found", "Carta nao encontrada")
        attempts_count = (
            await session.execute(
                select(func.count(Guess.id)).where(Guess.letter_id == letter.id)
            )
        ).scalar_one()
        letter.attempts_count = attempts_count
        return letter

    async def update(
        self,
        session: AsyncSession,
        letter_id: int,
        content: str | None,
        anonymous_hint: str | None,
        is_revealed: bool | None,
        is_solved: bool | None,
    ) -> Letter:
        letter = await self.get(session, letter_id)
        if content is not None:
            letter.content = content
        if anonymous_hint is not None:
            letter.anonymous_hint = anonymous_hint
        if is_revealed is not None:
            letter.is_revealed = is_revealed
        if is_solved is not None:
            letter.is_solved = is_solved
            letter.solved_at = datetime.utcnow() if is_solved else None
        await session.commit()
        await session.refresh(letter)
        return letter

    async def delete(self, session: AsyncSession, letter_id: int) -> None:
        stmt = delete(Letter).where(Letter.id == letter_id)
        result = await session.execute(stmt)
        if result.rowcount == 0:
            raise NotFoundError("letter_not_found", "Carta nao encontrada")
        await session.commit()
