"""Central place to read settings from `.env`, with tutorial defaults."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    neo4j_uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7690")
    neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "graphrag123")
    ollama_url: str = os.getenv("OLLAMA_URL", "http://127.0.0.1:11435")
    chat_model: str = os.getenv("CHAT_MODEL", "qwen3.8:27b")
    embed_model: str = os.getenv("EMBED_MODEL", "nomic-embed-text")
    embed_dim: int = int(os.getenv("EMBED_DIM", "768"))


settings = Settings()
