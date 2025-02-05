from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.constants import ERROR_MESSAGE_ENTITY_NOT_FOUND
from app.entities.auth.constants import ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
)
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import (
    assign_platform_to_organization,
    assign_user_to_organization,
    create_random_organization,
)
from tests.utils.platform import create_random_platform
from tests.utils.users import get_user_by_email

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,assign_organization",
    [
        ("admin_user", False),
        pytest.param(
            "manager_user",
            False,
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS
            ),
        ),
        pytest.param(
            "manager_user",
            True,
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS
            ),
        ),
        pytest.param(
            "unverified_user",
            False,
            marks=pytest.mark.xfail(reason=ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED),
        ),
    ],
)
async def test_delete_platform_as_user(
    client_user: Any,
    assign_organization: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_organization = await create_random_organization(db_session)
    a_platform = await create_random_platform(db_session)
    await assign_platform_to_organization(db_session, a_platform.id, a_organization.id)
    if assign_organization:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
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
    assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]
