"""Configuration module for the application.

This module provides configuration settings using Pydantic's BaseSettings.
It loads configuration from environment variables and provides default values.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings.

    Attributes:
        VERSION: Application version.
        ENVIRONMENT: Environment (development, staging, production).
        SECRET_KEY: Secret key for JWT token encoding.
        ALGORITHM: Algorithm used for JWT token encoding.
        ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time in minutes.
        DEFAULT_ADMIN_USERNAME: Default admin username.
        DEFAULT_ADMIN_PASSWORD: Default admin password.
        DATABASE_URL: Database connection URL.
        DB_ECHO: Whether to echo SQL statements.
    """

    LOG_LEVEL: str = "INFO"

    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEFAULT_ADMIN_USERNAME: str = "admin"
    DEFAULT_ADMIN_PASSWORD: str = "admin"
    DATABASE_URL: str = "sqlite+aiosqlite:///./sql_app.db"
    DB_ECHO: bool = False


@lru_cache()
def get_settings() -> Settings:
    """Get application settings.

    Returns:
        Settings: Application settings instance.
    """
    return Settings()


settings = get_settings()
