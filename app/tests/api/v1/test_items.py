from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas import ItemRead
from app.tests.utils.item import create_random_item
from app.tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


async def test_create_item(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    data: Dict[str, str] = {"title": "Testing", "content": "One. Two.. Three..."}
    response: Response = await client.post(
        "items/", headers=superuser_token_headers, json=data
    )
    assert response.status_code == 200
    content: Dict[str, Any] = response.json()
    assert content["title"] == data["title"]
    assert content["content"] == data["content"]
    assert "id" in content
    assert "user_id" in content


async def test_read_item(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    item: ItemRead = await create_random_item(db_session)
    response: Response = await client.get(
        f"items/{item.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    content: Dict[str, Any] = response.json()
    assert content["title"] == item.title
    assert content["content"] == item.content
    assert content["id"] == str(item.id)
    assert content["user_id"] == str(item.user_id)


async def test_update_item(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    item: ItemRead = await create_random_item(db_session)
    new_title: str = random_lower_string()
    new_content: str = random_lower_string()
    data: Dict[str, str] = {"title": new_title, "content": new_content}
    response: Response = await client.patch(
        f"items/{item.id}", headers=superuser_token_headers, json=data
    )
    assert response.status_code == 200
    content: Dict[str, Any] = response.json()
    assert content["title"] != item.title
    assert content["title"] == new_title
    assert content["content"] != item.content
    assert content["content"] == new_content
    assert content["id"] == str(item.id)
    assert content["user_id"] == str(item.user_id)


async def test_delete_item(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    item: ItemRead = await create_random_item(db_session)
    response: Response = await client.delete(
        f"items/{item.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content: Dict[str, Any] = response.json()
    assert content["title"] == item.title
    assert content["content"] == item.content
    assert content["id"] == str(item.id)
    assert content["user_id"] == str(item.user_id)


async def test_list_items(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    item_1: ItemRead = await create_random_item(db_session)  # noqa: F841
    item_2: ItemRead = await create_random_item(db_session)  # noqa: F841
    item_3: ItemRead = await create_random_item(db_session)  # noqa: F841
    response: Response = await client.get("items/", headers=superuser_token_headers)
    assert 200 <= response.status_code < 300
    all_items: Dict[str, Any] = response.json()
    assert len(all_items) > 1
    for api_item in all_items:
        assert "id" in api_item
        assert "title" in api_item
        assert "content" in api_item
        assert "user_id" in api_item
