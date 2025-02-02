from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import (
    DB_STR_64BIT_MAXLEN_INPUT,
    DB_STR_DESC_MAXLEN_INPUT,
    DB_STR_TINYTEXT_MAXLEN_INPUT,
)
from app.entities.auth.constants import ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED
from app.entities.client.constants import ERROR_MESSAGE_CLIENT_EXISTS
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user",
    [
        ("admin_user"),
        ("manager_user"),
        ("employee_user"),
        ("client_a_user"),
        ("client_b_user"),
        pytest.param(
            "unverified_user",
            marks=pytest.mark.xfail(reason=ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED),
        ),
    ],
)
async def test_create_client_as_user(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    slug: str = random_lower_string(8)
    title: str = random_lower_string()
    description: str = random_lower_string()
    data: dict[str, str] = {"slug": slug, "title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=current_user.token_headers,
        json=data,
    )
    entry: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["slug"] == slug
    assert entry["title"] == title
    assert entry["description"] == description


@pytest.mark.parametrize(
    "slug,title,description,exists_by",
    [
        (
            random_lower_string(8),
            random_lower_string(),
            random_lower_string(),
            "title",
        ),
        (
            random_lower_string(8),
            random_lower_string(),
            random_lower_string(),
            "slug",
        ),
    ],
)
async def test_create_client_as_superuser_client_aleady_exists(
    slug: str,
    title: str,
    description: str,
    exists_by: str,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    data: dict[str, str] = {"slug": slug, "title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_user.token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: dict[str, Any] = response.json()
    assert entry["slug"] == slug
    assert entry["title"] == title
    assert entry["description"] == description
    data_2: dict[str, str]
    if exists_by == "title":
        slug_2: str = random_lower_string(8)
        description_2: str = random_lower_string()
        data_2: dict[str, str] = {
            "slug": slug_2,
            "title": title,
            "description": description_2,
        }
    if exists_by == "slug":
        title_2: str = random_lower_string()
        description_2: str = random_lower_string()
        data_2: dict[str, str] = {
            "slug": slug,
            "title": title_2,
            "description": description,
        }
    response_2: Response = await client.post(
        "clients/",
        headers=admin_user.token_headers,
        json=data_2,
    )
    assert response_2.status_code == 400
    entry_2: dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ERROR_MESSAGE_CLIENT_EXISTS


@pytest.mark.parametrize(
    "slug,title,description,error_msg",
    [
        (
            random_lower_string(2),
            random_lower_string(),
            random_lower_string(),
            "Value error, slug must be 3 characters or more",
        ),
        (
            random_lower_string(65),
            random_lower_string(),
            random_lower_string(),
            f"Value error, slug must be {DB_STR_64BIT_MAXLEN_INPUT} characters or less",
        ),
        (
            random_lower_string(8),
            random_lower_string(4),
            random_lower_string(),
            "Value error, title must be 5 characters or more",
        ),
        (
            random_lower_string(8),
            random_lower_string() * 100,
            random_lower_string(),
            f"Value error, title must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less",
        ),
        (
            random_lower_string(8),
            random_lower_string(),
            random_lower_string() * 160,
            f"Value error, description must be {DB_STR_DESC_MAXLEN_INPUT} characters or less",
        ),
    ],
)
async def test_create_client_as_superuser_client_limits(
    slug: str,
    title: str,
    description: str,
    error_msg: str,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    data: dict[str, str] = {"slug": slug, "title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_user.token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == error_msg
