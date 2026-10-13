# Backend image. Built for linux/amd64 because cadquery-ocp 7.9.x (required by
# CadQuery 2.8) has no Linux arm64 wheel; see docs/ENVIRONMENT.md (R1).
FROM --platform=linux/amd64 python:3.12-slim

# OpenGL/X libraries needed by the OCP and VTK wheels at import time.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgl1 libglu1-mesa libxrender1 libxext6 libx11-6 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /usr/local/bin/uv

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-dev --no-install-project
COPY autevra ./autevra
COPY migrations ./migrations
COPY alembic.ini ./
RUN uv sync --locked --no-dev

ENV AUTEVRA_DATA_DIR=/data PATH="/app/.venv/bin:$PATH"
VOLUME /data
EXPOSE 8000
CMD ["uvicorn", "--factory", "autevra.main:app", "--host", "0.0.0.0", "--port", "8000"]
