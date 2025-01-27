from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import ErrorCode
from app.models import User
from app.schemas import ClientRead, PlatformRead
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
    "client_user,assign_client",
    [
        ("admin_user", False),
        pytest.param(
            "manager_user",
            False,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
        pytest.param(
            "manager_user",
            True,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
        pytest.param(
            "unverified_user",
            False,
            marks=pytest.mark.xfail(reason=ErrorCode.UNVERIFIED_ACCESS_DENIED),
        ),
    ],
)
async def test_delete_platform_as_user(
    client_user: Any,
    assign_client: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_client: ClientRead = await create_random_client(db_session)
    a_platform: PlatformRead = await create_random_platform(db_session)
    await assign_platform_to_client(db_session, a_platform.id, a_client.id)
    if assign_client:
        this_user: User = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_client(db_session, this_user.id, a_client.id)
    response: Response = await client.delete(
        f"platforms/{a_platform.id}",
        headers=current_user.token_headers,
    )
    assert 200 <= response.status_code < 300
    response: Response = await client.get(
        f"platforms/{a_platform.id}",
        headers=current_user.token_headers,
    )
    assert response.status_code == 404
    data: dict[str, Any] = response.json()
    assert ErrorCode.ENTITY_NOT_FOUND in data["detail"]
