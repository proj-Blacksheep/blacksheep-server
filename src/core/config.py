from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.

    Attributes:
        PROJECT_NAME: Name of the project
        DEBUG: Debug mode flag
        API_V1_STR: API version path
        DATABASE_URL: SQLite database URL
    """

    model_config = SettingsConfigDict(env_file=".env")

    PROJECT_NAME: str = "FastAPI Template"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = "sqlite:///./sql_app.db"

    # JWT 토큰 생성 시 사용할 비밀 키
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DEFAULT_ADMIN_USERNAME: str = "admin"
    DEFAULT_ADMIN_PASSWORD: str = "admin"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
