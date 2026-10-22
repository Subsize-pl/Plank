import asyncio
from uuid import UUID

import pytest
from sqlalchemy import make_url

from api.app.settings import Settings
from api.repositories.seed import BOARD_ID
from api.run_seed import run_seed


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"

@pytest.fixture
def test_db_url() -> str:
   settings = Settings()
   db_url = settings.database_url

   if make_url(db_url).database != "plank_test":
       raise RuntimeError("The test is permitted only in plank_test")

   return db_url

@pytest.fixture
def seeded_board_id(test_db_url: str) -> UUID:
    asyncio.run(run_seed())
    return BOARD_ID


