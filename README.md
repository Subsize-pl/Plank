# Plank

A realtime kanban board: FastAPI + PostgreSQL backend, web frontend (planned).

## Layout

- `api/` — FastAPI backend (`app`, `services`, `repositories`, `ranking`, `realtime`)
- `ui/` — frontend (planned)
- `infra/` — deployment configs (planned)
- `docs/` — project documentation

## Getting started

```bash
cp .env.example .env
docker compose up --build
```

API docs: http://localhost:8000/docs

## Development (without Docker)

```bash
uv sync
uv run uvicorn api.app.main:app --reload
uv run pytest
```
