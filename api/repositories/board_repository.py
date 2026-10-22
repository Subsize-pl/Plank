from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from api.repositories import models


async def get_board_by_id(session: AsyncSession, board_id: UUID) -> models.Board | None:
    select_board_stmt = (
        select(models.Board)
        .outerjoin(models.Column, models.Board.id == models.Column.board_id)
        .outerjoin(
            models.Card,
            and_(
                models.Column.id == models.Card.column_id,
                models.Card.archived_at.is_(None),
            ),
        )
        .options(contains_eager(models.Board.columns).contains_eager(models.Column.cards))
        .where(models.Board.id == board_id)
        .order_by(
            models.Column.rank,
            models.Column.id,
            models.Card.rank,
            models.Card.id,
        )
    )

    query_result = await session.execute(select_board_stmt)
    selected_board = query_result.unique().scalar_one_or_none()

    return selected_board
