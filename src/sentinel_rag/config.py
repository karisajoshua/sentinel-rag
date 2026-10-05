from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SentinelRAG"
    environment: str = "development"
    api_prefix: str = "/api/v1"
    database_url: str | None = None
    openai_api_key: str | None = None
    openai_chat_model: str = "gpt-5-mini"

    model_config = SettingsConfigDict(
        env_prefix="SENTINEL_",
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
