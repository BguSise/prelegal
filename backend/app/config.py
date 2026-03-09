import os
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    # Database
    database_url: str = "sqlite:///./data/prelegal.db"

    # Auth - SECRET_KEY must be set in environment; no default allowed
    secret_key: str = Field(..., min_length=32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # API
    openrouter_api_key: str = ""

    # Paths
    templates_dir: str = "/app/templates"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
