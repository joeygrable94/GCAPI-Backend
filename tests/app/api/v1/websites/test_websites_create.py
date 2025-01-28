import unittest.mock
from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import ErrorCode
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.utils import random_boolean, random_domain

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
            marks=pytest.mark.xfail(reason=ErrorCode.UNVERIFIED_ACCESS_DENIED),
        ),
    ],
)
async def test_create_website_as_user(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    domain: str = random_domain(16, "com")
    is_secure: bool = random_boolean()
    data: dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    with unittest.mock.patch(
        "app.crud.website.WebsiteRepository.validate"
    ) as mock_validate_website_domain:
        mock_validate_website_domain.return_value = True
        response: Response = await client.post(
            "websites/",
            headers=current_user.token_headers,
            json=data,
        )
        entry: dict[str, Any] = response.json()
        assert 200 <= response.status_code < 300
        entry: dict[str, Any] = response.json()
        assert entry["domain"] == domain
        assert entry["is_secure"] == is_secure


async def test_create_website_as_superuser_website_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    domain: str = random_domain(16, "com")
    is_secure: bool = random_boolean()
    data: dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    with unittest.mock.patch(
        "app.crud.website.WebsiteRepository.validate"
    ) as mock_validate_website_domain:
        mock_validate_website_domain.return_value = True
        response: Response = await client.post(
            "websites/",
            headers=admin_user.token_headers,
            json=data,
        )
        assert 200 <= response.status_code < 300
        entry: dict[str, Any] = response.json()
        assert entry["domain"] == domain
        assert entry["is_secure"] == is_secure
    is_secure_2: bool = random_boolean()
    data_2: dict[str, Any] = {"domain": domain, "is_secure": is_secure_2}
    response_2: Response = await client.post(
        "websites/",
        headers=admin_user.token_headers,
        json=data_2,
    )
    assert response_2.status_code == 400
    entry_2: dict[str, Any] = response_2.json()
    assert ErrorCode.ENTITY_EXISTS in entry_2["detail"]


@pytest.mark.parametrize(
    "domain,is_secure,status_code,error_type,error_msg,check_domain",
    [
        pytest.param(
            random_domain(16, "co"),
            random_boolean(),
            400,
            "message",
            ErrorCode.DOMAIN_INVALID,
            True,
            marks=pytest.mark.xfail(reason=ErrorCode.DOMAIN_INVALID),
        ),
        (
            random_domain(1, "co"),
            random_boolean(),
            422,
            "detail",
            "Value error, domain must be 5 characters or more",
            False,
        ),
        (
            random_domain(DB_STR_TINYTEXT_MAXLEN_INPUT + 1, "com"),
            random_boolean(),
            422,
            "detail",
            f"Value error, domain must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less",  # noqa: E501
            False,
        ),
        (
            "https://" + random_domain(3, "pub"),
            random_boolean(),
            422,
            "detail",
            "Value error, invalid domain provided, top-level domain names and subdomains only accepted (example.com, sub.example.com)",  # noqa: E501
            False,
        ),
    ],
)
async def test_create_website_as_superuser_website_limits(
    domain: str,
    is_secure: bool,
    status_code: int,
    error_type: str,
    error_msg: str,
    check_domain: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    data: dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response
    with unittest.mock.patch(
        "app.crud.website.WebsiteRepository.validate"
    ) as mock_validate_website_domain:
        mock_validate_website_domain.return_value = check_domain
        response = await client.post(
            "websites/",
            headers=admin_user.token_headers,
            json=data,
        )
    assert response.status_code == status_code
    entry: dict[str, Any] = response.json()
    if error_type == "message":
        assert error_msg in entry["detail"]
    if error_type == "detail":
        assert error_msg in entry["detail"][0]["msg"]


async def test_create_website_as_superuser_website_domain_invalid(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    domain: str = random_domain(16, "com")
    is_secure: bool = random_boolean()
    data: dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response
    response = await client.post(
        "websites/",
        headers=admin_user.token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: dict[str, Any] = response.json()
    assert entry["detail"] == ErrorCode.DOMAIN_INVALID
