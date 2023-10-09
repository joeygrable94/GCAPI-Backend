from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_boolean, random_lower_string
from tests.utils.websites import create_random_website

from app.api.exceptions import ErrorCode
from app.schemas import WebsiteRead, WebsiteUpdate

pytestmark = pytest.mark.asyncio


async def test_update_website_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: WebsiteRead = await create_random_website(db_session)
    new_is_secure: bool = random_boolean()
    update_dict = WebsiteUpdate(is_secure=new_is_secure)
    response: Response = await client.patch(
        f"websites/{entry_a.id}",
        headers=superuser_token_headers,
        json=update_dict.model_dump(),
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["id"] == str(entry_a.id)
    assert entry["domain"] == entry_a.domain
    assert entry["is_secure"] == new_is_secure


async def test_update_website_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: WebsiteRead = await create_random_website(db_session)
    entry_b: WebsiteRead = await create_random_website(db_session)
    update_dict = WebsiteUpdate(domain=entry_b.domain, is_secure=random_boolean())
    response: Response = await client.patch(
        f"websites/{entry_a.id}",
        headers=superuser_token_headers,
        json=update_dict.model_dump(),
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_entry["detail"] == ErrorCode.WEBSITE_DOMAIN_EXISTS


async def test_update_website_as_superuser_domain_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: WebsiteRead = await create_random_website(db_session)
    new_domain: str = "a.co"
    data: Dict[str, Any] = {"domain": new_domain, "is_secure": random_boolean()}
    response: Response = await client.patch(
        f"websites/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"] == "Value error, domain must be 5 characters or more"
    )


async def test_update_website_as_superuser_domain_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: WebsiteRead = await create_random_website(db_session)
    new_domain: str = random_lower_string() * 10 + ".com"
    data: Dict[str, Any] = {"domain": new_domain, "is_secure": random_boolean()}
    response: Response = await client.patch(
        f"websites/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == "Value error, domain must be 255 characters or less"
    )


async def test_update_website_as_superuser_domain_invalid(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: WebsiteRead = await create_random_website(db_session)
    new_domain: str = "https://" + random_lower_string() + ".com"
    data: Dict[str, Any] = {"domain": new_domain, "is_secure": random_boolean()}
    response: Response = await client.patch(
        f"websites/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == "Value error, invalid domain provided, top-level domain names and subdomains only accepted (example.com, sub.example.com)"  # noqa: E501
    )
