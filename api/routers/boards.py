from collections.abc import Awaitable, Callable
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from api.app.dependencies import get_board_service
from api.schemas.boards import BoardGet

router = APIRouter(prefix="/api/v1/boards", tags=["boards"])


@router.get("/{board_id}")
async def read_board(
    board_id: UUID,
    board_service: Annotated[Callable[[UUID], Awaitable[BoardGet]], Depends(get_board_service)],
) -> BoardGet:

    response_board = await board_service(board_id)

    return response_board
