# Plank

A realtime kanban board: FastAPI + PostgreSQL backend, web frontend (planned).

## Layout

- `api/` — FastAPI backend (`app`, `services`, `repositories`, `ranking`, `realtime`)
- `ui/` — frontend (planned)
- `infra/` — deployment configs (planned)
- `docs/` — project documentation

## Getting started with Docker

Requirements: Docker with Docker Compose.

Run the following commands from the repository root in PowerShell.

Create the local configuration file if it does not exist:

```powershell
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
}
```

Adjust `.env` if you need different database credentials or published ports.

Build and start PostgreSQL and the API:

```powershell
docker compose up --build -d
```

Apply database migrations before using the board endpoints:

```powershell
docker compose exec api uv run --no-sync alembic upgrade head
```

Optionally populate the database with demonstration data:

```powershell
docker compose exec api uv run --no-sync python -m api.run_seed
```

With the default API port:

- API documentation: http://localhost:8000/docs
- Health endpoint: http://localhost:8000/health

If you changed `API_PORT`, use that port in these URLs.

To inspect API logs:

```powershell
docker compose logs -f api
```

## Development without a Docker API container

The API runs locally; PostgreSQL still runs through Docker Compose.

Run the commands from the repository root in PowerShell.

If the API container is already running, stop it to free port 8000:

```powershell
docker compose stop api
```

Install the locked dependencies and start PostgreSQL:

```powershell
uv sync --frozen
docker compose up -d --wait db
```

Set the database URL in the current terminal:

```powershell
$env:DATABASE_URL = "postgresql+asyncpg://plank:plank@localhost:5432/plank"
```

This example uses the defaults from `.env.example`. Adjust the username,
password, database name and published port if you changed them.

The local application reads `DATABASE_URL` from the environment;
it does not automatically load `.env`.

Apply migrations and start the API:

```powershell
uv run --no-sync alembic upgrade head
uv run --no-sync uvicorn api.app.main:app --reload
```

The default API documentation URL is http://localhost:8000/docs.

Inside Docker Compose, PostgreSQL is available as `db:5432`.
From the host computer, use `localhost` and the published PostgreSQL port.
