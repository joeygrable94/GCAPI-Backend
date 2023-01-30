from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_boolean, random_lower_string
from tests.utils.websites import create_random_website

from app.db.schemas import WebsiteRead, WebsiteUpdate

pytestmark = pytest.mark.asyncio


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
        json=update_dict.dict(),
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_entry["detail"] == "Website domain exists"


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
    assert entry["detail"][0]["msg"] == "domain must contain 5 or more characters"


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
    assert entry["detail"][0]["msg"] == "domain must contain less than 255 characters"


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
        == "invalid domain provided, top-level domain names and subdomains only accepted (example.com, sub.example.com)"  # noqa: E501
    )
