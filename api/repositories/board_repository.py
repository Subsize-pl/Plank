from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories import models


async def get_board_by_id(session: AsyncSession, board_id: UUID) -> models.Board | None:
    stmt = select(models.Board).where(models.Board.id == board_id)
    query_result = await session.execute(stmt)
    selected_board = query_result.scalar_one_or_none()
    return selected_board





