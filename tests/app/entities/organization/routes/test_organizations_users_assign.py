from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.core_organization.constants import (
    ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
)
from app.entities.core_user.constants import ERROR_MESSAGE_USER_NOT_FOUND
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION,
)
from app.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import create_random_organization
from tests.utils.users import create_random_user, get_user_by_email

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
async def test_organization_assign_random_user_as_user(
    client_user: Any,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_user = await create_random_user(db_session)
    a_organization = await create_random_organization(db_session)
    a_user_organization = {
        "user_id": str(a_user.id),
        "organization_id": str(a_organization.id),
    }
    response: Response = await client.post(
        f"organizations/{a_organization.id}/assign/user",
        headers=current_user.token_headers,
        json=a_user_organization,
    )
    assert response.status_code == status_code
    data: dict[str, Any] = response.json()
    assert data["id"] is not None
    assert data["user_id"] == str(a_user.id)
    assert data["organization_id"] == str(a_organization.id)


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
async def test_organization_assign_current_user_to_organization(
    client_user: Any,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    this_user = await get_user_by_email(db_session, current_user.email)
    a_organization = await create_random_organization(db_session)
    a_user_organization = {
        "user_id": str(this_user.id),
        "organization_id": str(a_organization.id),
    }
    response: Response = await client.post(
        f"organizations/{a_organization.id}/assign/user",
        headers=current_user.token_headers,
        json=a_user_organization,
    )
    assert response.status_code == status_code
    data: dict[str, Any] = response.json()
    assert data["id"] is not None
    assert data["user_id"] == str(this_user.id)
    assert data["organization_id"] == str(a_organization.id)


@pytest.mark.parametrize(
    "client_user",
    [
        ("admin_user"),
        ("manager_user"),
        pytest.param(
            "employee_user",
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION
            ),
        ),
    ],
)
async def test_organization_assign_user_as_user_missmatching_organization_id(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    this_user = await get_user_by_email(db_session, current_user.email)
    a_organization_bad_id = get_uuid_str()
    a_organization = await create_random_organization(db_session)
    user_organization_in = {
        "user_id": str(this_user.id),
        "organization_id": a_organization_bad_id,
    }
    response: Response = await client.post(
        f"organizations/{a_organization.id}/assign/user",
        headers=current_user.token_headers,
        json=user_organization_in,
    )
    assert response.status_code == 404
    data: dict[str, Any] = response.json()
    assert data["detail"] == ERROR_MESSAGE_ORGANIZATION_NOT_FOUND


@pytest.mark.parametrize(
    "client_user",
    [
        ("admin_user"),
        ("manager_user"),
        pytest.param(
            "employee_user",
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION
            ),
        ),
    ],
)
async def test_organization_assign_user_as_user_user_not_exists(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user = request.getfixturevalue(client_user)
    bad_user_id = get_uuid_str()
    a_organization = await create_random_organization(db_session)
    user_organization_in = {
        "user_id": bad_user_id,
        "organization_id": str(a_organization.id),
    }
    response: Response = await client.post(
        f"organizations/{a_organization.id}/assign/user",
        headers=current_user.token_headers,
        json=user_organization_in,
    )
    assert response.status_code == 404
    data: dict[str, Any] = response.json()
    assert data["detail"] == ERROR_MESSAGE_USER_NOT_FOUND
