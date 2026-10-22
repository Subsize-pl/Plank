from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import make_url

from api.app.main import create_app
from api.app.settings import Settings

NOT_FOUND_BOARD_ID = UUID("01a12d46-799b-7e82-8a0a-af401d97afab")
DB_BOARD_ID = UUID("01a12d46-799b-7e82-8a0a-af401d97afaa")


def test_get_board_not_found():
    settings = Settings()
    db_url = settings.database_url

    if make_url(db_url).database != "plank_test":
        raise RuntimeError("The test is permitted only in plank_test")

    with TestClient(create_app()) as client:
        response = client.get(f"/api/v1/boards/{NOT_FOUND_BOARD_ID}")

        assert response.status_code == 404
        assert response.json() == {"detail": "Board not found"}


def test_get_board_by_returns_tree():
    settings = Settings()
    db_url = settings.database_url

    if make_url(db_url).database != "plank_test":
        raise RuntimeError("The test is permitted only in plank_test")


