# One-line commands for Autevra. Run `make help` for the list.
.PHONY: help setup dev backend frontend test test-backend test-frontend lint format docker docker-up clean

BACKEND_PORT ?= 8000

help:
	@echo "make setup     install backend (uv) and frontend (npm) dependencies"
	@echo "make dev       run the backend (:$(BACKEND_PORT)) and the frontend (:5173) with reload"
	@echo "make test      backend pytest + frontend vitest"
	@echo "make lint      ruff check/format check + TypeScript check"
	@echo "make format    apply ruff formatting"
	@echo "make docker    build the Docker images (backend is linux/amd64)"
	@echo "make docker-up run the Compose stack on http://localhost:8080"

setup:
	cd backend && uv sync
	cd frontend && npm ci --no-fund --no-audit

backend:
	cd backend && uv run uvicorn --factory autevra.main:app --reload --port $(BACKEND_PORT)

frontend:
	cd frontend && npm run dev

dev:
	@trap 'kill 0' INT TERM EXIT; \
	$(MAKE) --no-print-directory backend & \
	$(MAKE) --no-print-directory frontend & \
	wait

test: test-backend test-frontend

test-backend:
	cd backend && uv run pytest -q

test-frontend:
	cd frontend && npm test

lint:
	cd backend && uv run ruff check . && uv run ruff format --check .
	cd frontend && npm run typecheck

format:
	cd backend && uv run ruff format . && uv run ruff check --fix .

docker:
	docker compose build

docker-up:
	docker compose up --build

clean:
	rm -rf backend/.pytest_cache backend/.ruff_cache frontend/dist
