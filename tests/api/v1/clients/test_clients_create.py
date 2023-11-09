from typing import Any
from typing import Dict

import pytest
from httpx import AsyncClient
from httpx import Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string

from app.api.exceptions import ErrorCode

pytestmark = pytest.mark.asyncio


async def test_create_client_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    title: str = random_lower_string()
    description: str = random_lower_string()
    data: Dict[str, str] = {"title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == title
    assert entry["description"] == description


async def test_create_client_as_superuser_client_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    title: str = random_lower_string()
    description: str = random_lower_string()
    data: Dict[str, str] = {"title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["title"] == title
    assert entry["description"] == description
    description_2: str = random_lower_string()
    data_2: Dict[str, str] = {"title": title, "description": description_2}
    response_2: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ErrorCode.CLIENT_EXISTS


async def test_create_client_as_superuser_client_title_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    title: str = "1234"
    description: str = random_lower_string()
    data: Dict[str, str] = {"title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"] == "Value error, title must be 5 characters or more"
    )


async def test_create_client_as_superuser_client_title_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    title: str = random_lower_string() * 4
    description: str = random_lower_string()
    data: Dict[str, str] = {"title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"] == "Value error, title must be 96 characters or less"
    )


async def test_create_client_as_superuser_client_description_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    title: str = random_lower_string()
    description: str = random_lower_string() * 160
    data: Dict[str, str] = {"title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == "Value error, description must be 5000 characters or less"
    )  # noqa: E501
