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
        pytest.param(
            "manager_user",
            False,
            False,
            405,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
        ("manager_user", True, False, 200),
        pytest.param(
            "manager_user",
            True,
            True,
            405,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
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
)
async def test_delete_tracking_link_as_user(
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
    await create_random_tracking_link(db_session, client_a.id)
    a_link = await create_random_tracking_link(db_session, client_a.id)
    b_link = await create_random_tracking_link(db_session, client_b.id)
    delete_link_id = a_link.id
    if assign_client:
        this_user: User = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_client(db_session, this_user.id, client_a.id)
        if assign_wrong_client:
            delete_link_id = b_link.id
    response: Response = await client.delete(
        f"utmlinks/{delete_link_id}",
        headers=current_user.token_headers,
    )
    assert response.status_code == status_code
