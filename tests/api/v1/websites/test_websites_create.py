from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.users import create_new_user, get_current_user_tokens
from tests.utils.utils import random_boolean, random_domain, random_lower_string

from app.api.errors import ErrorCode
from app.db.schemas.user import UserAdmin
from app.security.auth.manager import AuthManager

pytestmark = pytest.mark.asyncio


async def test_create_website_as_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    domain: str = random_domain()
    is_secure: bool = random_boolean()
    data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["domain"] == domain
    assert entry["is_secure"] == is_secure


async def test_create_website_as_superuser_website_already_exists(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    domain: str = random_domain()
    is_secure: bool = random_boolean()
    data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["domain"] == domain
    assert entry["is_secure"] == is_secure
    is_secure_2: bool = random_boolean()
    data_2: Dict[str, Any] = {"domain": domain, "is_secure": is_secure_2}
    response_2: Response = await client.post(
        "websites/",
        headers=superuser_token_headers,
        json=data_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == "Website domain exists"


async def test_create_website_as_testuser(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserAdmin
    a_user_password: str
    a_user, a_user_password = await create_new_user(user_auth)
    a_user_access_header = await get_current_user_tokens(
        client, a_user.email, a_user_password
    )
    a_token: str = a_user_access_header["access_token"]
    domain: str = random_domain()
    is_secure: bool = random_boolean()
    data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers={"Authorization": f"Bearer {a_token}"},
        json=data,
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS


async def test_create_website_as_superuser_domain_too_short(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    domain: str = "a.co"
    is_secure: bool = random_boolean()
    data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "domain must contain 5 or more characters"


async def test_create_website_as_superuser_domain_too_long(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    domain: str = random_lower_string() * 10 + ".com"
    is_secure: bool = random_boolean()
    data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "domain must contain less than 255 characters"


async def test_create_website_as_superuser_domain_is_not_valid_domain(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    domain: str = "https://src.pub"
    is_secure: bool = random_boolean()
    data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == "invalid domain provided, top-level domain names and subdomains only accepted (example.com, sub.example.com)"  # noqa: E501
    )
