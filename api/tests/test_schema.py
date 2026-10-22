from uuid import UUID

import pytest
from sqlalchemy import make_url, select
from sqlalchemy.exc import IntegrityError

from api.app.settings import Settings
from api.repositories import models
from api.repositories.database import Database
from api.repositories.models import Card
from api.repositories.seed import seed

TEST_COLUMN_ID = UUID("01a12d46-799b-7000-8000-000000000102")


@pytest.mark.anyio
async def test_seed_rank_order():
    settings = Settings()
    db_url = settings.database_url

    if make_url(db_url).database != "plank_test":
        raise RuntimeError("The test is permitted only in plank_test")

    database = Database(db_url)

    try:
        async with database.session_factory() as session:
            await seed(session)

        async with database.session_factory() as session:
            stmt = select(Card.rank).order_by(Card.rank, Card.id)
            query_result = await session.execute(stmt)
            result = query_result.scalars().all()
            expected_ranks = [
                "a0",
                "a1",
                "a2",
                "a3",
                "a4",
                "a5",
                "a6",
                "a7",
                "a8",
                "a9",
            ]
            assert result == expected_ranks
    finally:
        await database.close()


@pytest.mark.anyio
async def test_card_rejects_unknown_column_id():
    settings = Settings()
    db_url = settings.database_url

    if make_url(db_url).database != "plank_test":
        raise RuntimeError("The test is permitted only in plank_test")

    database = Database(db_url)

    try:
        async with database.session_factory() as session:
            assert await session.get(models.Column, TEST_COLUMN_ID) is None

            card = models.Card(
                id=UUID("01a12d46-799b-7000-8000-000000000101"),
                title="test_card_title",
                description="test_card_description",
                rank="a1",
                version=2,
                column_id=TEST_COLUMN_ID,
            )

            session.add(card)
            with pytest.raises(IntegrityError):
                await session.flush()

            await session.rollback()

    finally:
        await database.close()
