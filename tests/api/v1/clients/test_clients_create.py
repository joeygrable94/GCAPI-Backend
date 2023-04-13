from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.utils import random_lower_string

from app.api.errors import ErrorCode

pytestmark = pytest.mark.asyncio


async def test_create_client_as_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    title: str = random_lower_string()
    content: str = random_lower_string()
    data: Dict[str, str] = {"title": title, "content": content}
    response: Response = await client.post(
        "clients/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["title"] == title
    assert entry["content"] == content


async def test_create_client_as_superuser_client_already_exists(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    title: str = random_lower_string()
    content: str = random_lower_string()
    data: Dict[str, str] = {"title": title, "content": content}
    response: Response = await client.post(
        "clients/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["title"] == title
    assert entry["content"] == content
    content_2: str = random_lower_string()
    data_2: Dict[str, str] = {"title": title, "content": content_2}
    response_2: Response = await client.post(
        "clients/",
        headers=superuser_token_headers,
        json=data_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ErrorCode.CLIENT_EXISTS


async def test_create_client_as_superuser_client_title_too_short(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    title: str = "1234"
    content: str = random_lower_string()
    data: Dict[str, str] = {"title": title, "content": content}
    response: Response = await client.post(
        "clients/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "title must contain 5 or more characters"


async def test_create_client_as_superuser_client_title_too_long(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    title: str = random_lower_string() * 4
    content: str = random_lower_string()
    data: Dict[str, str] = {"title": title, "content": content}
    response: Response = await client.post(
        "clients/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "title must contain less than 96 characters"


async def test_create_client_as_superuser_client_content_too_long(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    title: str = random_lower_string()
    content: str = random_lower_string() * 10
    data: Dict[str, str] = {"title": title, "content": content}
    response: Response = await client.post(
        "clients/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "content must contain less than 255 characters"
