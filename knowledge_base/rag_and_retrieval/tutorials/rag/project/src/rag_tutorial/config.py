"""Central place to read settings from `.env`, with tutorial defaults."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / ".env", extra="ignore")

    ollama_url: str = "http://127.0.0.1:11435"
    chat_model: str = "qwen3.8:27b"
    embed_model: str = "nomic-embed-text"
    embed_dim: int = 768
    qdrant_url: str = "http://localhost:6343"
    cache_dir: str = "data/cache"
    project_root: Path = PROJECT_ROOT

    def path(self, rel: str | Path) -> Path:
        """Resolve a path relative to the project root."""
        return self.project_root / rel


settings = Settings()
