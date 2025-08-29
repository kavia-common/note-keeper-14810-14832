"""
Application settings management.

Loads configuration from environment variables and .env using pydantic-settings.
"""

from functools import lru_cache
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# Load .env at import time to ensure environment is populated for settings
load_dotenv()


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    database_url: str = Field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./notes.db"),
        description="SQLAlchemy database URL (e.g., sqlite:///./notes.db)",
    )
    cors_allow_origins: str = Field(
        default_factory=lambda: os.getenv("CORS_ALLOW_ORIGINS", "*"),
        description="Comma-separated list of CORS origins, or *",
    )


# PUBLIC_INTERFACE
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
