from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.constants import ERROR_MESSAGE_ENTITY_EXISTS
from app.entities.core_organization.constants import (
    ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
)
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
)
from app.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import (
    assign_user_to_organization,
    create_random_organization,
)
from tests.utils.tracking_link import create_random_tracking_link
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,assign_organization,assign_wrong_client,status_code",
    [
        ("admin_user", False, False, 200),
        ("manager_user", False, False, 200),
        ("client_a_user", False, False, 200),
        ("client_a_user", True, False, 200),
        pytest.param(
            "client_a_user",
            True,
            True,
            405,
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS
            ),
        ),
        ("employee_user", True, False, 200),
        ("verified_user", False, False, 200),
        ("verified_user", True, False, 200),
        pytest.param(
            "verified_user",
            True,
            True,
            405,
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS
            ),
        ),
    ],
)
async def test_create_tracking_link_as_user(
    client_user: Any,
    assign_organization: bool,
    assign_wrong_client: bool,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    await create_random_tracking_link(db_session, a_organization.id)
    await create_random_tracking_link(db_session, a_organization.id)
    await create_random_tracking_link(db_session, b_organization.id)
    a_url = "https://example.com/destination&utm_campaign=campaign-name&utm_medium=medium-name&utm_source=source-name&utm_content=content-name&utm_term=term-name"
    data_in = {
        "url": a_url,
        "is_active": True,
    }
    if assign_organization:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
        if assign_wrong_client:
            data_in["organization_id"] = str(b_organization.id)
        else:
            data_in["organization_id"] = str(a_organization.id)
    response: Response = await client.post(
        "utmlinks/",
        headers=current_user.token_headers,
        json=data_in,
    )
    assert response.status_code == status_code


async def test_create_tracking_link_as_superuser_already_exists(
    admin_user: ClientAuthorizedUser,
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    a_link = await create_random_tracking_link(db_session, a_organization.id)
    await create_random_tracking_link(db_session, a_organization.id)
    await create_random_tracking_link(db_session, b_organization.id)
    data_in = {
        "url": a_link.url,
        "is_active": True,
    }
    response: Response = await client.post(
        "utmlinks/",
        headers=admin_user.token_headers,
        json=data_in,
    )
    data = response.json()
    assert response.status_code == 400
    assert ERROR_MESSAGE_ENTITY_EXISTS in data["detail"]


async def test_create_tracking_link_as_superuser_organization_not_found(
    admin_user: ClientAuthorizedUser,
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    a_organization = await create_random_organization(db_session)
    client_b = get_uuid_str()
    await create_random_tracking_link(db_session, a_organization.id)
    await create_random_tracking_link(db_session, a_organization.id)
    link_url = "/" + random_lower_string(16)
    data_in = {
        "url": link_url,
        "is_active": True,
        "organization_id": client_b,
    }
    response: Response = await client.post(
        "utmlinks/",
        headers=admin_user.token_headers,
        json=data_in,
    )
    data = response.json()
    assert response.status_code == 404
    assert ERROR_MESSAGE_ORGANIZATION_NOT_FOUND == data["detail"]
