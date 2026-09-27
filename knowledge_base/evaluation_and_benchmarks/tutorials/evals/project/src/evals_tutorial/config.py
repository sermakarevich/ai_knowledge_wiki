"""Central place to read settings from `.env`, with tutorial defaults."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / ".env", extra="ignore")

    ollama_url: str = "http://127.0.0.1:11435"
    chat_model: str = "qwen3.8:27b"
    judge_model: str = "qwen3.8:27b"
    embed_model: str = "nomic-embed-text"
    cache_dir: str = "data/cache"
    project_root: Path = PROJECT_ROOT

    # Chapter 13: Langfuse self-hosted stack (see docker-compose.yml, profile
    # `langfuse`; UI on http://localhost:3030). Empty default = tracing stays
    # a no-op until the keys are set in .env.
    langfuse_host: str = ""
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""

    def path(self, rel: str | Path) -> Path:
        """Resolve a path relative to the project root."""
        return self.project_root / rel


settings = Settings()

