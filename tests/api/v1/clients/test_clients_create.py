from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string

from app.api.exceptions import ErrorCode
from app.db.constants import (
    DB_STR_64BIT_MAXLEN_INPUT,
    DB_STR_DESC_MAXLEN_INPUT,
    DB_STR_TINYTEXT_MAXLEN_INPUT,
)

pytestmark = pytest.mark.asyncio


async def test_create_client_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    slug: str = random_lower_string(8)
    title: str = random_lower_string()
    description: str = random_lower_string()
    data: Dict[str, str] = {"slug": slug, "title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["slug"] == slug
    assert entry["title"] == title
    assert entry["description"] == description


async def test_create_client_as_superuser_client_already_exists_by_title(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    slug: str = random_lower_string(8)
    title: str = random_lower_string()
    description: str = random_lower_string()
    data: Dict[str, str] = {"slug": slug, "title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["slug"] == slug
    assert entry["title"] == title
    assert entry["description"] == description
    description_2: str = random_lower_string()
    slug_2: str = random_lower_string(8)
    data_2: Dict[str, str] = {
        "slug": slug_2,
        "title": title,
        "description": description_2,
    }
    response_2: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ErrorCode.CLIENT_EXISTS


async def test_create_client_as_superuser_client_already_exists_by_slug(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    slug: str = random_lower_string(8)
    title: str = random_lower_string()
    description: str = random_lower_string()
    data: Dict[str, str] = {"slug": slug, "title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["slug"] == slug
    assert entry["title"] == title
    assert entry["description"] == description
    title_2: str = random_lower_string()
    description_2: str = random_lower_string()
    data_2: Dict[str, str] = {
        "slug": slug,
        "title": title_2,
        "description": description_2,
    }
    response_2: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ErrorCode.CLIENT_EXISTS


async def test_create_client_as_superuser_client_slug_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    slug: str = random_lower_string(2)
    title: str = random_lower_string()
    description: str = random_lower_string()
    data: Dict[str, str] = {"slug": slug, "title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == "Value error, slug must be 3 characters or more"  # noqa: E501
    )


async def test_create_client_as_superuser_client_slug_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    slug: str = random_lower_string(65)
    title: str = random_lower_string()
    description: str = random_lower_string()
    data: Dict[str, str] = {"slug": slug, "title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, slug must be {DB_STR_64BIT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )


async def test_create_client_as_superuser_client_title_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    slug: str = random_lower_string(8)
    title: str = "1234"
    description: str = random_lower_string()
    data: Dict[str, str] = {"slug": slug, "title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == "Value error, title must be 5 characters or more"  # noqa: E501
    )


async def test_create_client_as_superuser_client_title_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    slug: str = random_lower_string(8)
    title: str = random_lower_string() * 100
    description: str = random_lower_string()
    data: Dict[str, str] = {"slug": slug, "title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, title must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )


async def test_create_client_as_superuser_client_description_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    slug: str = random_lower_string(8)
    title: str = random_lower_string()
    description: str = random_lower_string() * 160
    data: Dict[str, str] = {"slug": slug, "title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, description must be {DB_STR_DESC_MAXLEN_INPUT} characters or less"  # noqa: E501
    )
