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


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
