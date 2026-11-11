"""FastAPI application factory."""

import threading
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse

from autevra import __version__, domains, extensions
from autevra.ai.llm.clients import LLMClient, make_client
from autevra.api import access
from autevra.api.aerospace import router as aerospace_router
from autevra.api.change import router as change_router
from autevra.api.installs import router as installs_router
from autevra.api.inventory import router as inventory_router
from autevra.api.mechanical import router as mechanical_router
from autevra.api.product import router as product_router
from autevra.api.routes import EXCEPTION_HANDLERS, router
from autevra.api.service import Workspace
from autevra.api.structures import router as structures_router
from autevra.api.surfaces import router as surfaces_router
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
    if settings.warm_up:
        threading.Thread(target=app.state.workspace.warm_up, daemon=True).start()
    # Model payloads are mostly mesh numbers and compress about 3:1.
    app.add_middleware(GZipMiddleware, minimum_size=1000)
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
    app.include_router(surfaces_router, prefix="/api")
    app.include_router(structures_router, prefix="/api")
    app.include_router(aerospace_router, prefix="/api")
    app.include_router(product_router, prefix="/api")
    app.include_router(inventory_router, prefix="/api")
    app.include_router(mechanical_router, prefix="/api")
    app.include_router(installs_router, prefix="/api")
    app.include_router(change_router, prefix="/api")

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    if settings.static_dir is not None:
        _serve_studio(app, settings.static_dir)
    return app


def _serve_studio(app: FastAPI, root: Path) -> None:
    """Serve the built studio from ``root``: files as they are, and ``index.html`` for every
    other non-API path (client-side routes such as /studio/<id>/aircraft)."""
    root = root.resolve()
    index = root / "index.html"
    if not index.is_file():
        raise RuntimeError(f"no built studio at {root} (run the frontend build first)")

    @app.get("/{path:path}", include_in_schema=False)
    def studio(path: str) -> FileResponse:
        if path.startswith("api/"):
            raise HTTPException(status_code=404)
        target = (root / path).resolve()
        if path and target.is_file() and target.is_relative_to(root):
            return FileResponse(target)
        return FileResponse(index)


def app() -> FastAPI:
    """Factory for ``uvicorn --factory autevra.main:app``."""
    return create_app()
