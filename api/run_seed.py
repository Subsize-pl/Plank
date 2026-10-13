import asyncio

from api.app.settings import Settings
from api.repositories.database import Database
from api.repositories.seed import seed


async def run_seed() -> None:
    settings = Settings()
    db_url = settings.database_url
    database = Database(db_url)
    try:
        async with database.session_factory() as session:
            await seed(session)
    finally:
        await database.close()


if __name__ == "__main__":
    asyncio.run(run_seed())
