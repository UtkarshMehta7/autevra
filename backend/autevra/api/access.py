"""Access rules for a public instance: visitor workspaces and request limits.

Locally every setting is off and nothing here changes behaviour. On a hosted demo
(``AUTEVRA_WORKSPACE_ISOLATION=true``) each browser generates a random workspace key and
sends it as ``X-Autevra-Workspace``; projects are stored with the key's SHA-256 and are
visible only to requests carrying the same key. A project of another workspace answers
404, exactly like a project that does not exist.

This is isolation between anonymous visitors, not authentication: whoever has the key
(it lives in the browser's local storage) has the projects.
"""

import hashlib
import re
import threading
import time
from collections import deque
from dataclasses import dataclass

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from autevra.config import Settings
from autevra.storage.repository import ProjectNotFoundError

HEADER = "X-Autevra-Workspace"
_KEY = re.compile(r"^[A-Za-z0-9_-]{16,128}$")


@dataclass(frozen=True)
class Visitor:
    owner: str | None  # SHA-256 of the workspace key; None when isolation is off
    isolated: bool

    @property
    def all_owners(self) -> bool:
        return not self.isolated


def _settings(request: Request) -> Settings:
    return request.app.state.settings


def visitor(request: Request) -> Visitor:
    if not _settings(request).workspace_isolation:
        return Visitor(None, False)
    key = request.headers.get(HEADER, "")
    if not _KEY.match(key):
        raise HTTPException(
            status_code=400,
            detail=f"this instance keeps each visitor's projects separate; send {HEADER} "
            "(the website does this for you, so reload the page)",
        )
    return Visitor(hashlib.sha256(key.encode()).hexdigest(), True)


def guard_project(request: Request) -> None:
    """Router-wide dependency: a project in the path must belong to the visitor."""
    project_id = request.path_params.get("project_id")
    if project_id is None or not _settings(request).workspace_isolation:
        return
    owner = visitor(request).owner
    if request.app.state.workspace.project_owner(project_id) != owner:
        raise ProjectNotFoundError(project_id)


def check_project_quota(request: Request, who: Visitor) -> None:
    limit = _settings(request).max_projects_per_workspace
    if who.isolated and limit and request.app.state.workspace.project_count(who.owner) >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"this workspace already has {limit} projects; delete one to make another",
        )


class SlidingWindow:
    """At most ``limit`` events per ``window`` seconds for each key, in memory."""

    def __init__(self, limit: int, window: float, max_keys: int = 10_000) -> None:
        self.limit, self.window, self.max_keys = limit, window, max_keys
        self._events: dict[str, deque[float]] = {}
        self._lock = threading.Lock()

    def retry_after(self, key: str, now: float | None = None) -> float:
        """0 if the event is allowed (and records it), else seconds until it would be."""
        now = time.monotonic() if now is None else now
        with self._lock:
            if len(self._events) >= self.max_keys and key not in self._events:
                self._prune(now)
            events = self._events.setdefault(key, deque())
            while events and now - events[0] >= self.window:
                events.popleft()
            if len(events) >= self.limit:
                return self.window - (now - events[0])
            events.append(now)
            return 0.0

    def _prune(self, now: float) -> None:
        for key in [k for k, ev in self._events.items() if not ev or now - ev[-1] >= self.window]:
            del self._events[key]
        while len(self._events) >= self.max_keys:  # still full: drop the oldest keys
            self._events.pop(next(iter(self._events)))


_WRITES = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def rate_limiter(settings: Settings):  # type: ignore[no-untyped-def]
    """HTTP middleware limiting writes per client address (reads are never limited)."""
    writes = SlidingWindow(settings.write_limit_per_minute, 60.0)
    contact = SlidingWindow(settings.contact_limit_per_hour, 3600.0)

    async def middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
        if request.method in _WRITES:
            client = request.client.host if request.client else "unknown"
            checks = [(writes, settings.write_limit_per_minute)]
            if request.url.path == "/api/contact":
                checks.append((contact, settings.contact_limit_per_hour))
            for window, limit in checks:
                wait = window.retry_after(client) if limit else 0.0
                if wait:
                    return JSONResponse(
                        status_code=429,
                        content={"detail": "too many changes in a short time; wait a moment"},
                        headers={"Retry-After": str(max(1, round(wait)))},
                    )
        return await call_next(request)

    return middleware
