"""Application entrypoint: the FastAPI app factory."""

from fastapi import FastAPI
from uvicorn import lifespan
from contextlib import asynccontextmanager

from settings import Settings
from ..repositories.database import Database


def create_app() -> FastAPI:
    """Create and configure the Plank API application."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        settings = Settings
        db_url = settings.database_url
        db = Database(db_url)
        try:




    app = FastAPI(title="Plank API", version="0.1.0", lifespan=lifespan)

    @app.get("/health")
    async def health() -> dict[str, str]:
        # Placeholder until KAN-25 wires in a real database check.
        return {"status": "ok"}

    return app


app = create_app()
