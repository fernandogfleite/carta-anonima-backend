from datetime import timedelta
from src.core.config.settings import get_settings

settings = get_settings()
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
DEFAULT_ACCESS_TOKEN_EXPIRE = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
