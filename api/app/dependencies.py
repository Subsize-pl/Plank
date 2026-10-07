from collections.abc import AsyncIterator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    db_object = request.app.state.database
    session = db_object.session_factory()
    async with session as session:
        yield session
