from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.core.utilities import get_uuid_str
from app.models.user import User
from app.schemas import ClientRead
from app.schemas.platform import PlatformRead
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import (
    assign_platform_to_client,
    assign_user_to_client,
    create_random_client,
)
from tests.utils.platform import create_random_platform
from tests.utils.users import get_user_by_email

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
            ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS,
        ),
    ],
)
async def test_read_platform_by_id_as_user(
    client_user: Any,
    assign_client: bool,
    status_code: int,
    error_type: str,
    error_msg: str,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_platform: PlatformRead = await create_random_platform(db_session)
    a_client: ClientRead = await create_random_client(db_session)
    await assign_platform_to_client(db_session, a_platform.id, a_client.id)
    if assign_client:
        this_user: User = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_client(db_session, this_user.id, a_client.id)
    response: Response = await client.get(
        f"platforms/{a_platform.id}",
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert status_code == response.status_code
    if error_type == "message":
        assert error_msg in data["detail"]
    if error_type == "detail":
        assert error_msg in data["detail"][0]["msg"]
    if error_type is None:
        assert data["id"] == str(a_platform.id)


async def test_read_platform_by_id_as_superuser_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"platforms/{entry_id}",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ErrorCode.ENTITY_NOT_FOUND in data["detail"]
