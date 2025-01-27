from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.models import User
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.tracking_link import create_random_tracking_link
from tests.utils.users import get_user_by_email

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,assign_client,assign_wrong_client,status_code",
    [
        ("admin_user", False, False, 200),
        ("manager_user", False, False, 200),
        pytest.param(
            "client_a_user",
            False,
            False,
            405,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
        ("client_a_user", True, False, 200),
        pytest.param(
            "client_a_user",
            True,
            True,
            405,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
        ("employee_user", True, False, 200),
        pytest.param(
            "verified_user",
            False,
            False,
            405,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
        ("verified_user", True, False, 200),
        pytest.param(
            "verified_user",
            True,
            True,
            405,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
    ],
    ids=[
        "admin user update any tracking link",
        "manager user update tracking link",
        "client_a user cannot update tracking link not assigned",
        "client_a user update tracking link assigned to client",
        "client_a user update tracking link assigned to wrong client",
        "employee user update tracking link assigned to client",
        "verified user update tracking link not assigned",
        "verified user update tracking link assigned to client",
        "verified user update tracking link assigned to wrong client",
    ],
)
async def test_update_tracking_link_as_user(
    client_user: Any,
    assign_client: bool,
    assign_wrong_client: bool,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    client_a = await create_random_client(db_session)
    client_b = await create_random_client(db_session)
    a_link = await create_random_tracking_link(db_session, client_a.id)
    await create_random_tracking_link(db_session, client_a.id)
    await create_random_tracking_link(db_session, client_b.id)
    a_url = "https://example.com/destination&utm_campaign=campaign-name&utm_medium=medium-name&utm_source=source-name&utm_content=content-name&utm_term=term-name"
    data_in = {
        "url": a_url,
        "is_active": True,
    }
    if assign_client:
        this_user: User = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_client(db_session, this_user.id, client_a.id)
        if assign_wrong_client:
            data_in["client_id"] = str(client_b.id)
        else:
            data_in["client_id"] = str(client_a.id)
    response: Response = await client.patch(
        f"utmlinks/{a_link.id}",
        headers=current_user.token_headers,
        json=data_in,
    )
    assert response.status_code == status_code


async def test_update_tracking_link_as_superuser_already_exists(
    admin_user: ClientAuthorizedUser,
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    client_a = await create_random_client(db_session)
    client_b = await create_random_client(db_session)
    a_link = await create_random_tracking_link(db_session, client_a.id)
    await create_random_tracking_link(db_session, client_a.id)
    b_link = await create_random_tracking_link(db_session, client_b.id)
    data_in = {
        "url": a_link.url,
        "is_active": True,
    }
    response: Response = await client.patch(
        f"utmlinks/{b_link.id}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    data = response.json()
    assert response.status_code == 400
    assert ErrorCode.ENTITY_EXISTS in data["detail"]
