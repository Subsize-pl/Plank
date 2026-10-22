from datetime import UTC, datetime
from uuid import UUID

import pytest
from sqlalchemy import event, make_url

from api.app.settings import Settings
from api.repositories import models
from api.repositories.board_repository import get_board_by_id
from api.repositories.database import Database

BOARD_ID = UUID("01a12d46-799b-7000-8000-000000002001")

user_data = {
    "id": UUID("01a12d46-799b-7000-8000-000000001001"),
    "username": "board_repository_test_user",
}

board_data = {
    "id": BOARD_ID,
    "owner_id": user_data["id"],
    "name": "Repository test board",
}

columns_data = [
    {
        # The empty column is added first but should be returned second.
        "id": UUID("01a12d46-799b-7000-8000-000000003002"),
        "board_id": board_data["id"],
        "name": "Done",
        "rank": "a1",
    },
    {
        "id": UUID("01a12d46-799b-7000-8000-000000003001"),
        "board_id": board_data["id"],
        "name": "To Do",
        "rank": "a0",
    },
]

cards_data = [
    {
        # This card should be returned last among the active cards.
        "id": UUID("01a12d46-799b-7000-8000-000000004003"),
        "column_id": columns_data[1]["id"],
        "title": "Write documentation",
        "description": None,
        "rank": "a1",
        "version": 1,
        "archived_at": None,
    },
    {
        # This archived card must not appear in the result.
        "id": UUID("01a12d46-799b-7000-8000-000000004004"),
        "column_id": columns_data[1]["id"],
        "title": "Archived task",
        "description": "This card must be excluded",
        "rank": "a0",
        "version": 2,
        "archived_at": datetime.now(UTC),
    },
    {
        # Two active cards have the same rank.
        # Their order should be determined by ID.
        "id": UUID("01a12d46-799b-7000-8000-000000004002"),
        "column_id": columns_data[1]["id"],
        "title": "Write tests",
        "description": "Check board loading",
        "rank": "a0",
        "version": 3,
        "archived_at": None,
    },
    {
        "id": UUID("01a12d46-799b-7000-8000-000000004001"),
        "column_id": columns_data[1]["id"],
        "title": "Implement board query",
        "description": "Load columns and active cards",
        "rank": "a0",
        "version": 1,
        "archived_at": None,
    },
]


@pytest.mark.anyio
async def test_get_board_by_id():
    settings = Settings()
    db_url = settings.database_url

    if make_url(db_url).database != "plank_test":
        raise RuntimeError("The test is permitted only in plank_test")

    database = Database(db_url)

    select_queries: list[str] = []

    @event.listens_for(database.engine.sync_engine, "before_cursor_execute")
    def record_select(_conn, _cursor, statement, _parameters, _context, _executemany):
        if statement.strip().upper().startswith("SELECT"):
            select_queries.append(statement)

    try:
        async with database.session_factory() as session:
            user = models.User(**user_data)
            board = models.Board(**board_data)

            columns = []

            for data in columns_data:
                column = models.Column(**data)
                columns.append(column)

            cards = []

            for data in cards_data:
                card = models.Card(**data)
                cards.append(card)

            session.add_all(
                (
                    user,
                    board,
                )
            )

            session.add_all(columns)
            session.add_all(cards)

            await session.flush()

            session.expunge_all()

            select_queries.clear()

            board_by_id = await get_board_by_id(session, BOARD_ID)

            assert board_by_id is not None

            assert board_by_id.id == board_data["id"]
            assert board_by_id.owner_id == board_data["owner_id"]
            assert board_by_id.name == board_data["name"]

            selected_column_ids = [column.id for column in board_by_id.columns]
            expected_column_ids = [columns_data[1]["id"], columns_data[0]["id"]]
            assert selected_column_ids == expected_column_ids
            assert board_by_id.columns[1].cards == []

            assert board_by_id.columns[0].cards[-1].id == cards_data[0]["id"]
            assert board_by_id.columns[0].cards[0].id == cards_data[-1]["id"]
            assert board_by_id.columns[0].cards[1].id == cards_data[-2]["id"]

            for card in board_by_id.columns[0].cards:
                assert card.id != cards_data[1]["id"]

            assert len(select_queries) == 1

            await session.rollback()

    finally:
        event.remove(
            database.engine.sync_engine,
            "before_cursor_execute",
            record_select,
        )
        await database.close()
