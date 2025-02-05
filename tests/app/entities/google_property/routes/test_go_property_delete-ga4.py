from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.constants import ERROR_MESSAGE_ENTITY_NOT_FOUND
from app.entities.go_property.schemas import GooglePlatformType
from app.services.permission.constants import ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS
from app.utilities import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.ga4 import create_random_ga4_property
from tests.utils.organizations import (
    assign_platform_to_organization,
    assign_user_to_organization,
    create_random_organization,
)
from tests.utils.platform import create_random_platform
from tests.utils.users import get_user_by_email

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,status_code,error_type,error_msg",
    [
        ("admin_user", 200, None, None),
        ("manager_user", 200, None, None),
        (
            "employee_user",
            403,
            "message",
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
        ),
    ],
)
async def test_delete_go_property_ga4_by_id_as_user(
    client_user: Any,
    status_code: int,
    error_type: str,
    error_msg: str,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    platform_type = GooglePlatformType.ga4.value
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_platform = await create_random_platform(db_session)
    a_organization = await create_random_organization(db_session)
    await assign_platform_to_organization(db_session, a_platform.id, a_organization.id)
    a_ga4_property = await create_random_ga4_property(
        db_session, a_organization.id, a_platform.id
    )
    this_user = await get_user_by_email(db_session, current_user.email)
    await assign_user_to_organization(db_session, this_user.id, a_organization.id)
    response: Response = await client.delete(
        f"go/{platform_type}/{a_ga4_property.id}",
        headers=current_user.token_headers,
    )
    data: dict[str, Any] | None = response.json()
    assert status_code == response.status_code
    if error_type == "message":
        assert error_msg in data["detail"]
    if error_type == "detail":
        assert error_msg in data["detail"][0]["msg"]
    if error_type is None:
        assert data is None


async def test_delete_go_property_ga4_by_id_as_superuser_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4.value
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"go/{platform_type}/{entry_id}",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]
