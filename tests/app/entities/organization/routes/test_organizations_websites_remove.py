from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.constants import ERROR_MESSAGE_ENTITY_NOT_FOUND
from app.entities.core_organization.constants import (
    ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
    ERROR_MESSAGE_ORGANIZATION_RELATIONSHOP_NOT_FOUND,
)
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION,
)
from app.utilities import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import (
    assign_website_to_organization,
    create_random_organization,
)
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,status_code",
    [
        ("admin_user", 200),
        ("manager_user", 200),
        pytest.param(
            "employee_user",
            403,
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION
            ),
        ),
    ],
)
async def test_organization_remove_random_website_as_user(
    client_user: Any,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_website = await create_random_website(db_session)
    a_organization = await create_random_organization(db_session)
    await assign_website_to_organization(db_session, a_website.id, a_organization.id)
    organization_website = {
        "organization_id": str(a_organization.id),
        "website_id": str(a_website.id),
    }
    response: Response = await client.post(
        f"organizations/{a_organization.id}/remove/website",
        headers=current_user.token_headers,
        json=organization_website,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == status_code
    assert data["id"] is not None
    assert data["organization_id"] == str(a_organization.id)
    assert data["website_id"] == str(a_website.id)


@pytest.mark.parametrize(
    "client_user,by_key_id,error_msg",
    [
        (
            "admin_user",
            "website_id",
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
        ),
        (
            "manager_user",
            "website_id",
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
        ),
        ("admin_user", "organization_id", ERROR_MESSAGE_ORGANIZATION_NOT_FOUND),
        ("manager_user", "organization_id", ERROR_MESSAGE_ORGANIZATION_NOT_FOUND),
        pytest.param(
            "employee_user",
            "website_id",
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION
            ),
        ),
    ],
)
async def test_organization_remove_website_as_user_missmatching_website_id(
    client_user: Any,
    by_key_id: str,
    error_msg: str,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_website = await create_random_website(db_session)
    a_organization = await create_random_organization(db_session)
    await assign_website_to_organization(db_session, a_website.id, a_organization.id)
    a_bad_key_id = get_uuid_str()
    organization_website: dict[str, str]
    if by_key_id == "website_id":
        organization_website = {
            "website_id": a_bad_key_id,
            "organization_id": str(a_organization.id),
        }
    if by_key_id == "organization_id":
        organization_website = {
            "website_id": str(a_website.id),
            "organization_id": a_bad_key_id,
        }
    response: Response = await client.post(
        f"organizations/{a_organization.id}/remove/website",
        headers=current_user.token_headers,
        json=organization_website,
    )
    assert response.status_code == 404
    data: dict[str, Any] = response.json()
    assert error_msg in data["detail"]


async def test_organization_remove_website_as_superuser_relation_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session)
    a_organization = await create_random_organization(db_session)
    organization_website = {
        "organization_id": str(a_organization.id),
        "website_id": str(a_website.id),
    }
    response: Response = await client.post(
        f"organizations/{a_organization.id}/remove/website",
        headers=admin_user.token_headers,
        json=organization_website,
    )
    assert response.status_code == 404
    data: dict[str, Any] = response.json()
    assert data["detail"] == ERROR_MESSAGE_ORGANIZATION_RELATIONSHOP_NOT_FOUND
