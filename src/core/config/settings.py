from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_origins(value: str) -> list[str]:
    if not value:
        return []
    return [origin.strip() for origin in value.split(",") if origin.strip()]


class Settings(BaseSettings):
    database_url: str = ""
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    admin_email: str = "admin@example.com"
    admin_name: str = "Admin"
    admin_password: str = "admin"
    spam_max_attempts: int = 3
    spam_window_seconds: int = 300
    backend_cors_origins: str = ""
    frontend_url: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    @property
    def cors_origins(self) -> list[str]:
        origins = _parse_origins(self.backend_cors_origins)
        if self.frontend_url:
            origins.append(self.frontend_url.strip())
        return list(dict.fromkeys(origins))


@lru_cache
def get_settings() -> Settings:
    return Settings()
