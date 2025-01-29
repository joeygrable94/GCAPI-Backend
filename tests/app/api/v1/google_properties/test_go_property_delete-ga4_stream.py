from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.core.utilities import get_uuid_str
from app.models.user import User
from app.schemas import ClientRead
from app.schemas.go import GooglePlatformType
from app.schemas.platform import PlatformRead
from app.schemas.website import WebsiteRead
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import (
    assign_platform_to_client,
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.ga4 import create_random_ga4_property, create_random_ga4_stream
from tests.utils.platform import create_random_platform
from tests.utils.users import get_user_by_email
from tests.utils.websites import create_random_website

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
            ErrorCode.INSUFFICIENT_PERMISSIONS,
        ),
    ],
)
async def test_delete_go_property_ga4_stream_by_id_as_user(
    client_user: Any,
    status_code: int,
    error_type: str,
    error_msg: str,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_platform: PlatformRead = await create_random_platform(db_session)
    a_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    await assign_platform_to_client(db_session, a_platform.id, a_client.id)
    a_ga4_property = await create_random_ga4_property(
        db_session, a_client.id, a_platform.id
    )
    a_ga4_stream = await create_random_ga4_stream(
        db_session, a_ga4_property.id, a_website.id
    )
    this_user: User = await get_user_by_email(db_session, current_user.email)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    await assign_website_to_client(db_session, a_website.id, a_client.id)
    response: Response = await client.delete(
        f"go/{platform_type}/{a_ga4_stream.id}",
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


async def test_delete_go_property_ga4_stream_by_id_as_superuser_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"go/{platform_type}/{entry_id}",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ErrorCode.ENTITY_NOT_FOUND in data["detail"]
