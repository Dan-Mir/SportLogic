from __future__ import annotations

from functools import lru_cache
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="ARENA_",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "SportLogic"
    env: str = "development"
    secret_key: str = "change-me"
    database_url: str = "postgresql+psycopg://arena:arena@localhost:5432/arena"
    redis_url: str = "redis://localhost:6379/0"
    modules_enabled: Annotated[list[str], NoDecode] = ["core"]
    ollama_url: str = "http://localhost:11434"
    openai_api_key: str = ""
    openai_base_url: str = ""
    brand_name: str = "SportLogic"
    brand_primary_color: str = "#2563eb"
    public_domain: str = "impianto.local"

    @field_validator("modules_enabled", mode="before")
    @classmethod
    def _split_modules(cls, value: object) -> object:
        if isinstance(value, str):
            return [s.strip() for s in value.split(",") if s.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
