"""Application settings loaded from the environment."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration shared by the application and Alembic."""

    DATABASE_URL: str
    SQL_ECHO: bool = False
    CORS_ORIGINS: str = "http://localhost:15173"

    @property
    def cors_origins(self) -> list[str]:
        """Return the explicitly configured browser origins."""

        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
