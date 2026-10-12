from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import api.repositories.models as models

USER_ID = UUID("01a12d46-799b-7993-b595-130399c7daad")
BOARD_ID = UUID("01a12d46-799b-7e82-8a0a-af401d97afaa")

TODO_COLUMN_ID = UUID("01a12d46-799b-7bb1-914c-8724812e83fe")
IN_PROGRESS_COLUMN_ID = UUID("01a12d46-799b-78f8-b081-48f8b7bc68f4")
DONE_COLUMN_ID = UUID("01a12d46-799b-7424-a520-189018344401")

CARD_1_ID = UUID("01a12d46-799b-7427-ad9b-1dcfac58db18")
CARD_2_ID = UUID("01a12d46-799b-74ce-87fd-97db7a90c999")
CARD_3_ID = UUID("01a12d46-799b-7a5f-b7a3-155a26b15f4a")
CARD_4_ID = UUID("01a12d46-799b-76b4-b169-e1c1e1dc52ef")
CARD_5_ID = UUID("01a12d46-799b-72a9-86ae-cfd1faeecfe3")
CARD_6_ID = UUID("01a12d46-799b-7ad9-8dcd-71f766e4f9b8")
CARD_7_ID = UUID("01a12d46-799b-75c1-907f-f3947a2e9cd0")
CARD_8_ID = UUID("01a12d46-799b-7385-90dc-2a3614d85772")
CARD_9_ID = UUID("01a12d46-799b-7fb5-99e5-bedac5b9a13a")
CARD_10_ID = UUID("01a12d46-799b-737e-a70f-4640bdc9d05c")


async def seed(session: AsyncSession) -> None:
    async with session.begin():
        user = await session.get(models.User, USER_ID)

        if user is None:
            user = models.User(
                id=USER_ID,
                username="plank1",
            )

        board = await session.get(models.Board, BOARD_ID)
        if board is None:
            board = models.Board(id=BOARD_ID, owner=user, board_name="plank1_board")

        to_do_column = await session.get(models.Column, TODO_COLUMN_ID)
        if to_do_column is None:
            to_do_column = models.Column(
                id=TODO_COLUMN_ID,
                column_name="To Do",
                rank="a0",
                board=board,
            )

        in_progress_column = await session.get(models.Column, IN_PROGRESS_COLUMN_ID)
        if in_progress_column is None:
            in_progress_column = models.Column(
                id=IN_PROGRESS_COLUMN_ID,
                column_name="In Progress",
                rank="a1",
                board=board,
            )

        done_column = await session.get(models.Column, DONE_COLUMN_ID)
        if done_column is None:
            done_column = models.Column(
                id=DONE_COLUMN_ID,
                column_name="Done",
                rank="a2",
                board=board,
            )

        card_data = [
            {
                "id": CARD_1_ID,
                "title": "card_1_title",
                "description": "card_1_description",
                "rank": "a0",
                "column": done_column,
            },
            {
                "id": CARD_2_ID,
                "title": "card_2_title",
                "description": "card_2_description",
                "rank": "a1",
                "column": done_column,
            },
            {
                "id": CARD_3_ID,
                "title": "card_3_title",
                "description": "card_3_description",
                "rank": "a2",
                "archived_at": datetime.now(UTC),
                "column": in_progress_column,
            },
            {
                "id": CARD_4_ID,
                "title": "card_4_title",
                "description": "card_4_description",
                "rank": "a3",
                "version": 2,
                "archived_at": datetime.now(UTC),
                "column": done_column,
            },
            {
                "id": CARD_5_ID,
                "title": "card_5_title",
                "description": "card_5_description",
                "rank": "a4",
                "column": in_progress_column,
            },
            {
                "id": CARD_6_ID,
                "title": "card_6_title",
                "description": "card_6_description",
                "rank": "a5",
                "version": 5,
                "archived_at": datetime.now(UTC),
                "column": to_do_column,
            },
            {
                "id": CARD_7_ID,
                "title": "card_7_title",
                "description": "card_7_description",
                "rank": "a6",
                "column": to_do_column,
            },
            {
                "id": CARD_8_ID,
                "title": "card_8_title",
                "description": "card_8_description",
                "rank": "a7",
                "version": 8,
                "archived_at": datetime.now(UTC),
                "column": done_column,
            },
            {
                "id": CARD_9_ID,
                "title": "card_9_title",
                "description": "card_9_description",
                "rank": "a8",
                "column": to_do_column,
            },
            {
                "id": CARD_10_ID,
                "title": "card_10_title",
                "description": "card_10_description",
                "rank": "a9",
                "version": 10,
                "archived_at": datetime.now(UTC),
                "column": in_progress_column,
            },
        ]

        card_ids = [data["id"] for data in card_data]

        stmt = select(models.Card.id).where(models.Card.id.in_(card_ids))

        query_result = await session.execute(stmt)
        existing_cards_ids = set(query_result.scalars().all())

        new_cards = []

        for data in card_data:
            if data["id"] not in existing_cards_ids:
                card = models.Card(**data)
                new_cards.append(card)

        session.add_all(
            (
                user,
                board,
                to_do_column,
                in_progress_column,
                done_column,
            )
        )
        session.add_all(new_cards)
