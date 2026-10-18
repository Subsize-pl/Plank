from uuid import UUID

import pytest
from pydantic import ValidationError

from api.schemas.boards import BoardGet, CardGet


def test_card_get():
    test_card_1 = CardGet(id=UUID("01a12d46-799b-7427-ad9b-1dcfac58db18"),
                        title="test_card_get_title_1",
                        rank="a0",
                        version=1
                        )

    assert test_card_1.model_dump() == {"id": UUID("01a12d46-799b-7427-ad9b-1dcfac58db18"),
                        "title": "test_card_get_title_1",
                        "description": None,
                        "rank": "a0",
                        "version": 1
                        }

    with pytest.raises(ValidationError):
        test_card_2 = CardGet(id=UUID("01a12d46-799b-7000-8000-000000000101"), #noqa: F841
                              title="test_card_get_title_2",
                              rank="a1",
                              version="w"
                              )

def test_board_get_with_columns_and_cards():
    board_data = {
        "id": "01a12d46-799b-7e82-8a0a-af401d97afaa",
        "name": "testing_board_name",
        "columns": [
            {
                "id": "01a12d46-799b-7bb1-914c-8724812e83fe",
                "name": "To Do",
                "rank": "a0",
                "cards": [
                    {
                        "id": "01a12d46-799b-7427-ad9b-1dcfac58db18",
                        "title": "Configure project",
                        "description": "Install libraries",
                        "rank": "a0",
                        "version": 1,
                    },
                    {
                        "id": "01a12d46-799b-79ae-9a6e-4fd34a1b5742",
                        "title": "Write some tests",
                        "rank": "a1",
                        "version": 2,
                    },
                ],
            },
            {
                "id": "01a12d46-799b-78f8-b081-48f8b7bc68f4",
                "name": "Done",
                "rank": "a1",
            },
        ],
    }

    expected_data = {
        "id": "01a12d46-799b-7e82-8a0a-af401d97afaa",
        "name": "testing_board_name",
        "columns": [
            {
                "id": "01a12d46-799b-7bb1-914c-8724812e83fe",
                "name": "To Do",
                "rank": "a0",
                "cards": [
                    {
                        "id": "01a12d46-799b-7427-ad9b-1dcfac58db18",
                        "title": "Configure project",
                        "description": "Install libraries",
                        "rank": "a0",
                        "version": 1,
                    },
                    {
                        "id": "01a12d46-799b-79ae-9a6e-4fd34a1b5742",
                        "title": "Write some tests",
                        "description": None,
                        "rank": "a1",
                        "version": 2,
                    },
                ],
            },
            {
                "id": "01a12d46-799b-78f8-b081-48f8b7bc68f4",
                "name": "Done",
                "rank": "a1",
                "cards": [],
            },
        ],
    }

    test_board = BoardGet.model_validate(board_data)

    assert test_board.model_dump(mode="json") == expected_data




