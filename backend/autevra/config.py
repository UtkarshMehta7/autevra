"""Settings read from environment variables (prefix ``AUTEVRA_``)."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AUTEVRA_", env_file=".env", extra="ignore")

    data_dir: Path = Path("data")
    database_url: str = ""
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # Local LLM fallback (Phase 2). "off" keeps the app fully deterministic.
    llm_provider: str = "ollama"  # ollama | llama_server | off
    llm_url: str = "http://127.0.0.1:11434"
    llm_model: str = "qwen3:1.7b"
    llm_timeout: float = 60.0

    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return f"sqlite:///{(self.data_dir / 'autevra.db').resolve()}"
