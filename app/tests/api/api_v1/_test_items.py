import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import config as settings
from app.tests.utils.item import create_random_item


@pytest.mark.asyncio
async def test_create_item(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = await client.post(
        f"{settings.API_PREFIX}/items/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


@pytest.mark.asyncio
async def test_read_item(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    item = await create_random_item(db)
    response = await client.get(
        f"{settings.API_PREFIX}/items/{item.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["id"] == item.id
    assert content["owner_id"] == item.owner_id
