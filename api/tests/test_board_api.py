from uuid import UUID

from fastapi.testclient import TestClient

from api.app.main import create_app

NOT_FOUND_BOARD_ID = UUID("01a12d46-799b-7e82-8a0a-af401d97afab")


def test_get_board_not_found(test_db_url: str):

    with TestClient(create_app()) as client:
        response = client.get(f"/api/v1/boards/{NOT_FOUND_BOARD_ID}")

        assert response.status_code == 404
        assert response.json() == {"detail": "Board not found"}


def test_get_board_by_returns_tree(seeded_board_id: UUID):

    with TestClient(create_app()) as client:
        response = client.get(f"/api/v1/boards/{seeded_board_id}")

        assert response.status_code == 200

        serialized_response = response.json()

        expected_data = {
            "id": "01a12d46-799b-7e82-8a0a-af401d97afaa",
            "name": "plank1_board",
            "columns": [
                {
                    "id": "01a12d46-799b-7bb1-914c-8724812e83fe",
                    "name": "To Do",
                    "rank": "a0",
                    "cards": [
                        {
                            "id": "01a12d46-799b-75c1-907f-f3947a2e9cd0",
                            "title": "card_7_title",
                            "description": "card_7_description",
                            "rank": "a6",
                            "version": 1,
                        },
                        {
                            "id": "01a12d46-799b-7fb5-99e5-bedac5b9a13a",
                            "title": "card_9_title",
                            "description": "card_9_description",
                            "rank": "a8",
                            "version": 1,
                        },
                    ],
                },
                {
                    "id": "01a12d46-799b-78f8-b081-48f8b7bc68f4",
                    "name": "In Progress",
                    "rank": "a1",
                    "cards": [
                        {
                            "id": "01a12d46-799b-72a9-86ae-cfd1faeecfe3",
                            "title": "card_5_title",
                            "description": "card_5_description",
                            "rank": "a4",
                            "version": 1,
                        },
                    ],
                },
                {
                    "id": "01a12d46-799b-7424-a520-189018344401",
                    "name": "Done",
                    "rank": "a2",
                    "cards": [
                        {
                            "id": "01a12d46-799b-7427-ad9b-1dcfac58db18",
                            "title": "card_1_title",
                            "description": "card_1_description",
                            "rank": "a0",
                            "version": 1,
                        },
                        {
                            "id": "01a12d46-799b-74ce-87fd-97db7a90c999",
                            "title": "card_2_title",
                            "description": "card_2_description",
                            "rank": "a1",
                            "version": 1,
                        },
                    ],
                },
            ],
        }

        assert serialized_response == expected_data
