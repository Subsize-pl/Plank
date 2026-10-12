import pytest
from sqlalchemy import make_url, select

from api.app.settings import Settings
from api.repositories.database import Database
from api.repositories.models import Card
from api.repositories.seed import seed


@pytest.mark.anyio
async def test_seed_rank_order() -> None:
    settings = Settings()
    db_url = settings.database_url

    if make_url(db_url).database != "plank_test":
        raise RuntimeError("Тест разрешён только в plank_test")

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
