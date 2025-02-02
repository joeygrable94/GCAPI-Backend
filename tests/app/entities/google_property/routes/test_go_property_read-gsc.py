from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.constants import ERROR_MESSAGE_ENTITY_NOT_FOUND
from app.entities.go_property.schemas import GooglePlatformType
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
)
from app.utilities import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import (
    assign_platform_to_client,
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.go_sc import create_random_go_search_console_property
from tests.utils.platform import create_random_platform
from tests.utils.users import get_user_by_email
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,assign_client,status_code,error_type,error_msg",
    [
        ("admin_user", False, 200, None, None),
        ("manager_user", False, 200, None, None),
        ("employee_user", True, 200, None, None),
        (
            "employee_user",
            False,
            405,
            "message",
            ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
        ),
    ],
)
async def test_read_go_property_gsc_by_id_as_user(
    client_user: Any,
    assign_client: bool,
    status_code: int,
    error_type: str,
    error_msg: str,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    platform_type = GooglePlatformType.gsc.value
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_platform = await create_random_platform(db_session)
    a_client = await create_random_client(db_session)
    a_website = await create_random_website(db_session)
    await assign_platform_to_client(db_session, a_platform.id, a_client.id)
    a_gsc_property = await create_random_go_search_console_property(
        db_session, a_client.id, a_website.id, a_platform.id
    )
    if assign_client:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_client(db_session, this_user.id, a_client.id)
        await assign_website_to_client(db_session, a_website.id, a_client.id)
    response: Response = await client.get(
        f"go/{platform_type}/{a_gsc_property.id}",
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert status_code == response.status_code
    if error_type == "message":
        assert error_msg in data["detail"]
    if error_type == "detail":
        assert error_msg in data["detail"][0]["msg"]
    if error_type is None:
        assert data["id"] == str(a_gsc_property.id)


async def test_read_go_property_gsc_by_id_as_superuser_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.gsc.value
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"go/{platform_type}/{entry_id}",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]
