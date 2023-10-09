from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.utils import random_boolean, random_domain

from app.api.exceptions import ErrorCode

pytestmark = pytest.mark.asyncio


async def test_create_website_as_superuser(
    celery_worker: Any,
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    domain: str = "joeygrable.com"
    is_secure: bool = random_boolean()
    data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["task_id"] is not None
    assert entry["website"]["domain"] == domain
    assert entry["website"]["is_secure"] == is_secure
    task_id = entry["task_id"]
    response: Response = await client.get(
        f"tasks/{task_id}",
        headers=superuser_token_headers,
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json == {
        "task_id": task_id,
        "task_status": "PENDING",
        "task_result": None,
    }


async def test_create_website_as_superuser_website_already_exists(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    domain: str = "oceanbrightconsulting.com"
    is_secure: bool = random_boolean()
    data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["task_id"] is not None
    assert entry["website"]["domain"] == domain
    assert entry["website"]["is_secure"] == is_secure
    is_secure_2: bool = random_boolean()
    data_2: Dict[str, Any] = {"domain": domain, "is_secure": is_secure_2}
    response_2: Response = await client.post(
        "websites/",
        headers=superuser_token_headers,
        json=data_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ErrorCode.WEBSITE_DOMAIN_EXISTS


async def test_create_website_as_superuser_domain_invalid(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    bad_domain: str = random_domain(16, "co")
    is_secure: bool = random_boolean()
    data: Dict[str, Any] = {"domain": bad_domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    entry: Dict[str, Any] = response.json()
    assert entry["detail"] == ErrorCode.WEBSITE_DOMAIN_INVALID


async def test_create_website_as_superuser_domain_too_short(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    domain: str = random_domain(1, "co")
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
        entry["detail"][0]["msg"] == "Value error, domain must be 5 characters or more"
    )


async def test_create_website_as_superuser_domain_too_long(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    domain: str = random_domain(255, "com")
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
        == "Value error, domain must be 255 characters or less"
    )


async def test_create_website_as_superuser_domain_is_not_valid_domain(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    domain: str = "https://" + random_domain(3, "pub")
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
        == "Value error, invalid domain provided, top-level domain names and subdomains only accepted (example.com, sub.example.com)"  # noqa: E501
    )
