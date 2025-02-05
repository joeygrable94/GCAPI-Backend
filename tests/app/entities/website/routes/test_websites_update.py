import unittest.mock
from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.entities.api.constants import ERROR_MESSAGE_ENTITY_EXISTS
from app.entities.auth.constants import ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED
from app.entities.website.constants import ERROR_MESSAGE_DOMAIN_INVALID
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION,
)
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import (
    assign_user_to_organization,
    assign_website_to_organization,
    create_random_organization,
)
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_domain, random_lower_string
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,assign_organization",
    [
        ("admin_user", False),
        ("manager_user", False),
        ("employee_user", True),
        ("client_a_user", True),
        pytest.param(
            "employee_user",
            False,
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION
            ),
        ),
        pytest.param(
            "client_a_user",
            False,
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION
            ),
        ),
        pytest.param(
            "unverified_user",
            False,
            marks=pytest.mark.xfail(reason=ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED),
        ),
    ],
)
async def test_update_website_as_user(
    client_user: Any,
    assign_organization: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_website = await create_random_website(db_session)
    a_website = await create_random_website(db_session)
    a_organization = await create_random_organization(db_session)
    await assign_website_to_organization(db_session, a_website.id, a_organization.id)
    if assign_organization:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
    update_dict = {"is_secure": not a_website.is_secure}
    response: Response = await client.patch(
        f"websites/{a_website.id}",
        headers=current_user.token_headers,
        json=update_dict,
    )
    assert 200 <= response.status_code < 300
    entry: dict[str, Any] = response.json()
    assert entry["id"] == str(a_website.id)
    assert entry["domain"] == a_website.domain
    assert entry["is_secure"] is not a_website.is_secure


@pytest.mark.parametrize(
    "domain,status_code,error_type,error_msg,check_domain",
    [
        pytest.param(
            None,
            400,
            "message",
            ERROR_MESSAGE_ENTITY_EXISTS,
            False,
        ),
        pytest.param(
            random_domain(16, "co"),
            400,
            "message",
            ERROR_MESSAGE_DOMAIN_INVALID,
            True,
            marks=pytest.mark.xfail(reason=ERROR_MESSAGE_DOMAIN_INVALID),
        ),
        pytest.param(
            "a.co",
            422,
            "detail",
            "Value error, domain must be 5 characters or more",
            False,
        ),
        pytest.param(
            random_lower_string() * 10 + ".com",
            422,
            "detail",
            "Value error, domain must be {} characters or less".format(
                DB_STR_TINYTEXT_MAXLEN_INPUT
            ),
            False,
        ),
        pytest.param(
            "https://" + random_lower_string() + ".com",
            422,
            "detail",
            "Value error, invalid domain provided, top-level domain names and subdomains only accepted (example.com, sub.example.com)",
            False,
        ),
    ],
)
async def test_update_website_as_superuser_website_limits(
    domain: str | None,
    status_code: int,
    error_type: str,
    error_msg: str,
    check_domain: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session)
    update_dict: dict[str, Any] = {"is_secure": not a_website.is_secure}
    if domain is None:
        update_dict = {"domain": a_website.domain, "is_secure": not a_website.is_secure}
    else:
        update_dict = {"domain": domain, "is_secure": not a_website.is_secure}

    response: Response
    with unittest.mock.patch(
        "app.entities.website.crud.WebsiteRepository.validate"
    ) as mock_validate_website_domain:
        mock_validate_website_domain.return_value = check_domain
        response: Response = await client.patch(
            f"websites/{a_website.id}",
            headers=admin_user.token_headers,
            json=update_dict,
        )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_type == "message":
        assert error_msg in entry["detail"]
    if error_type == "detail":
        assert error_msg in entry["detail"][0]["msg"]


async def test_update_website_as_superuser_website_domain_invalid(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session)
    domain: str = random_domain(16, "com")
    update_dict: dict[str, Any] = {
        "domain": domain,
        "is_secure": not a_website.is_secure,
    }
    response: Response
    response: Response = await client.patch(
        f"websites/{a_website.id}",
        headers=admin_user.token_headers,
        json=update_dict,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 422
    assert entry["detail"] == ERROR_MESSAGE_DOMAIN_INVALID
