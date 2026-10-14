"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from autevra import __version__, domains, extensions
from autevra.ai.llm.clients import LLMClient, make_client
from autevra.api import access
from autevra.api.routes import EXCEPTION_HANDLERS, router
from autevra.api.service import Workspace
from autevra.config import Settings
from autevra.storage.database import Database, migrate


def create_app(settings: Settings | None = None, llm: LLMClient | None = None) -> FastAPI:
    settings = settings or Settings()
    llm = llm or make_client(
        settings.llm_provider, settings.llm_url, settings.llm_model, settings.llm_timeout
    )
    domains.load_builtin()
    extensions.load(settings.plugin_modules(), use_entry_points=settings.plugin_entry_points)
    url = settings.resolved_database_url()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    migrate(url)

    app = FastAPI(title="Autevra", version=__version__)
    app.state.workspace = Workspace(Database(url), settings.data_dir, llm)
    app.state.settings = settings
    # Added before CORS so that CORS stays outermost and 429 answers carry its headers.
    app.middleware("http")(access.rate_limiter(settings))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    for exc_type, handler in EXCEPTION_HANDLERS.items():
        app.add_exception_handler(exc_type, handler)
    app.include_router(router)

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    return app


def app() -> FastAPI:
    """Factory for ``uvicorn --factory autevra.main:app``."""
    return create_app()
