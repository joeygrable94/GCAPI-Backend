from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import create_random_client
from tests.utils.platform import create_random_platform

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,status_code",
    [
        ("admin_user", 200),
        ("manager_user", 200),
        pytest.param(
            "employee_user",
            403,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACTION),
        ),
    ],
)
async def test_clients_assign_random_platform_as_user(
    client_user: Any,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_platform = await create_random_platform(db_session)
    a_client = await create_random_client(db_session)
    client_platform = {"client_id": str(a_client.id), "platform_id": str(a_platform.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/assign/platform",
        headers=current_user.token_headers,
        json=client_platform,
    )
    assert response.status_code == status_code
    if status_code == 200:
        data: dict[str, Any] = response.json()
        assert data["id"] is not None
        assert data["client_id"] == str(a_client.id)
        assert data["platform_id"] == str(a_platform.id)


@pytest.mark.parametrize(
    "client_user,by_key_id,error_msg",
    [
        (
            "admin_user",
            "platform_id",
            ErrorCode.ENTITY_NOT_FOUND,
        ),
        (
            "manager_user",
            "platform_id",
            ErrorCode.ENTITY_NOT_FOUND,
        ),
        ("admin_user", "client_id", ErrorCode.CLIENT_NOT_FOUND),
        ("manager_user", "client_id", ErrorCode.CLIENT_NOT_FOUND),
        pytest.param(
            "employee_user",
            "platform_id",
            ErrorCode.ENTITY_NOT_FOUND,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACTION),
        ),
    ],
)
async def test_clients_assign_platform_as_user_missmatching_platform_id(
    client_user: Any,
    by_key_id: str,
    error_msg: str,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_platform = await create_random_platform(db_session)
    a_client = await create_random_client(db_session)
    a_bad_key_id = get_uuid_str()
    client_platform: dict[str, str]
    if by_key_id == "platform_id":
        client_platform = {"platform_id": a_bad_key_id, "client_id": str(a_client.id)}
    if by_key_id == "client_id":
        client_platform = {"platform_id": str(a_platform.id), "client_id": a_bad_key_id}
    response: Response = await client.post(
        f"clients/{a_client.id}/assign/platform",
        headers=current_user.token_headers,
        json=client_platform,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert error_msg in data["detail"]
