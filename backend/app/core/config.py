"""
NovaMart — Application Configuration

Centralized settings management using Pydantic Settings.
All values are read from environment variables / .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ─── Application ─────────────────────────────────────
    APP_NAME: str = "NovaMart"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # ─── Database ────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://novamart_user:novamart_pass_2026@localhost:5433/novamart_db"

    # ─── JWT Authentication ──────────────────────────────
    JWT_SECRET_KEY: str = "change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ─── AI / Embeddings ─────────────────────────────────
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSIONS: int = 384

    @property
    def EMBEDDING_DIMENSION(self) -> int:
        return self.EMBEDDING_DIMENSIONS

    # ─── CORS ────────────────────────────────────────────
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # ─── Seeding ─────────────────────────────────────────
    SEED_ON_STARTUP: bool = True

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Singleton instance
settings = Settings()
