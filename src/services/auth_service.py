from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.utils.password import verify_password, hash_password
from src.utils.jwt import create_access_token
from src.core.exceptions.app_exceptions import AuthenticationError
from src.core.config.settings import get_settings


class AuthService:
    async def authenticate(
        self, session: AsyncSession, email: str, password: str
    ) -> str:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user is None or not verify_password(password, user.hashed_password):
            raise AuthenticationError("invalid_credentials", "Credenciais invalidas")
        token_payload = {"sub": str(user.id), "is_admin": user.is_admin}
        return create_access_token(token_payload)

    async def ensure_admin(self, session: AsyncSession) -> User:
        settings = get_settings()
        result = await session.execute(
            select(User).where(User.email == settings.admin_email)
        )
        user = result.scalar_one_or_none()
        if user:
            return user
        user = User(
            name=settings.admin_name,
            email=settings.admin_email,
            hashed_password=hash_password(settings.admin_password),
            is_admin=True,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
