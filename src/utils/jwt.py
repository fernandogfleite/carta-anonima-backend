from datetime import datetime, timedelta
from typing import Any
from jose import jwt
from src.core.config.settings import get_settings


def create_access_token(
    subject: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    settings = get_settings()
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, **subject}
    return jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def decode_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    return jwt.decode(
        token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
    )
