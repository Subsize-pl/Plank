"""Application entrypoint: the FastAPI app factory."""

from contextlib import asynccontextmanager
from typing import Annotated

from asyncpg import PostgresError
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.exc import TimeoutError as PoolTimeoutError
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.dependencies import get_session
from api.app.settings import Settings
from api.repositories.database import Database


def create_app() -> FastAPI:
    """Create and configure the Plank API application."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        settings = Settings()
        db_url = settings.database_url
        db = Database(db_url)
        app.state.database = db
        try:
            yield
        finally:
            await db.close()

    app = FastAPI(title="Plank API", version="0.1.0", lifespan=lifespan)

    @app.get("/health")
    async def health(
        session: Annotated[AsyncSession, Depends(get_session)], response: Response
    ) -> dict[str, str]:
        try:
            await session.execute(text("SELECT 1"))
        except (DBAPIError, PoolTimeoutError, OSError, PostgresError) as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is down",
            ) from exc

        response.status_code = status.HTTP_200_OK
        return {"status": "ok", "db": "ok"}

    return app


app = create_app()
