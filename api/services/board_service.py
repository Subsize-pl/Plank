from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.board_repository import get_board_by_id
from api.schemas.boards import BoardGet


async def get_board(session: AsyncSession, board_id: UUID) -> BoardGet:

    selected_board = await get_board_by_id(session, board_id)

    if selected_board is None:
        raise HTTPException(status_code=404, detail="Board not found")


