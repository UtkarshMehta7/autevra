#!/bin/sh
# Assemble the Hugging Face Space repository: the backend image sources plus the Space card.
# Usage: deploy/huggingface/build-space.sh <output-dir>
set -eu
root=$(cd "$(dirname "$0")/../.." && pwd)
out=${1:?usage: build-space.sh <output-dir>}
mkdir -p "$out"
cp "$root/deploy/huggingface/README.md" "$out/README.md"
cd "$root/backend"
cp Dockerfile .dockerignore .python-version pyproject.toml uv.lock alembic.ini "$out/"
# Source only: no caches, local data or tests.
tar --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' -cf - autevra migrations | tar -xf - -C "$out"
# The Space has no local LLM (no hosted inference is ever used), so the parser runs alone.
sed -i.bak 's/^USER autevra$/USER autevra\
ENV AUTEVRA_LLM_PROVIDER=off/' "$out/Dockerfile" && rm "$out/Dockerfile.bak"
grep -q '^ENV AUTEVRA_LLM_PROVIDER=off$' "$out/Dockerfile"
