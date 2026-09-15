# Dev image for the api service (KAN-6): hot reload, no production hardening.
# Build context is the repo root (see docker-compose.yml), so paths are relative to it.
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Keep the venv outside /app: the repo root is volume-mounted over /app in dev.
    UV_PROJECT_ENVIRONMENT=/opt/venv

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Dependencies first, so source edits don't invalidate this layer.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Only needed when the image runs without a volume mount; in dev the live
# source is mounted over it.
COPY api ./api

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
