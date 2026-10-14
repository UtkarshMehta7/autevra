"""Settings read from environment variables (prefix ``AUTEVRA_``)."""

import json
from pathlib import Path
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AUTEVRA_", env_file=".env", extra="ignore")

    data_dir: Path = Path("data")
    database_url: str = ""
    # A JSON list, a comma-separated list or one URL (hosting dashboards make all three easy).
    cors_origins: Annotated[list[str], NoDecode] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # Local LLM fallback (Phase 2). "off" keeps the app fully deterministic.
    llm_provider: str = "ollama"  # ollama | llama_server | off
    llm_url: str = "http://127.0.0.1:11434"
    llm_model: str = "qwen3:1.7b"
    llm_timeout: float = 60.0

    # Public hosting. With isolation on, every request carries a browser-generated workspace
    # key (header X-Autevra-Workspace) and sees only the projects created with it. Limits
    # are per client address; 0 turns a limit off. All off for local use.
    workspace_isolation: bool = False
    write_limit_per_minute: int = 0
    contact_limit_per_hour: int = 0
    max_projects_per_workspace: int = 0
    # Build the default geometry in the background at startup (hosted instances).
    warm_up: bool = False

    # Plugins: comma-separated module paths, e.g. "autevra.contrib.brake_discs", plus any
    # installed package that declares the "autevra.plugins" entry-point group.
    plugins: str = ""
    plugin_entry_points: bool = True

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _parse_origins(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        text = value.strip()
        if text.startswith("["):
            return json.loads(text)
        # Browsers send the origin without a trailing slash, so strip one if pasted.
        return [o.strip().strip("'\"").rstrip("/") for o in text.split(",") if o.strip()]

    def plugin_modules(self) -> list[str]:
        return [m.strip() for m in self.plugins.split(",") if m.strip()]

    def resolved_database_url(self) -> str:
        if self.database_url:
            return normalise_database_url(self.database_url)
        return f"sqlite:///{(self.data_dir / 'autevra.db').resolve()}"


def normalise_database_url(url: str) -> str:
    """Hosted Postgres (Neon, Render, Heroku-style) hands out ``postgres://`` or
    ``postgresql://`` URLs; SQLAlchemy needs the driver named to use psycopg 3."""
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url.removeprefix(prefix)
    return url
