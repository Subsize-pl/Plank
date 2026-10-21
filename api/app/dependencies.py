from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.boards import BoardGet
from api.services.board_service import get_board


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    db_object = request.app.state.database
    session = db_object.session_factory()
    async with session as session:
        yield session


async def get_board_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Callable[[UUID], Awaitable[BoardGet]]:

    async def inner(board_id: UUID) -> BoardGet:
        board = await get_board(session, board_id)
        return board

    return inner
