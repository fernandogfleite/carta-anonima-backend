from fastapi import Depends, Header
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config.database import get_db_session
from src.core.config.settings import get_settings
from src.core.exceptions.app_exceptions import AuthenticationError, AuthorizationError
from src.models.user import User
from sqlalchemy import select


async def get_current_user(
    authorization: str | None = Header(default=None),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise AuthenticationError("missing_token", "Token de autenticacao ausente")
    token = authorization.split(" ", 1)[1]
    settings = get_settings()
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
    except JWTError as exc:
        raise AuthenticationError("invalid_token", "Token invalido") from exc
    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationError("invalid_token", "Token invalido")
    result = await session.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise AuthenticationError("invalid_user", "Usuario nao encontrado")
    return user


async def require_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise AuthorizationError("not_admin", "Acesso restrito")
    return current_user


# Backward-compatible alias to avoid breaking imports
require_admin = require_admin_user
