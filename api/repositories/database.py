"""Database resources owned by the application."""

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)


class Database:
    def __init__(self, url: str) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url,
            pool_pre_ping=True,
            pool_timeout=3,
            connect_args={"timeout": 3},
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    async def close(self) -> None:
        await self.engine.dispose()
