from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.organization.constants import ERROR_MESSAGE_ORGANIZATION_NOT_FOUND
from app.entities.organization.crud import OrganizationRepository
from app.utilities import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import (
    assign_user_to_organization,
    create_random_organization,
)
from tests.utils.users import get_user_by_email

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,status_code",
    [
        ("admin_user", 200),
        ("manager_user", 200),
        ("employee_user", 200),
        ("verified_user", 403),
    ],
)
async def test_read_organization_by_id_as_user(
    client_user: Any,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    this_user = await get_user_by_email(db_session, current_user.email)
    a_organization = await create_random_organization(db_session)
    await assign_user_to_organization(db_session, this_user.id, a_organization.id)
    response: Response = await client.get(
        f"organizations/{a_organization.id}",
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if status_code == 200:
        assert data["id"] == str(a_organization.id)
        repo = OrganizationRepository(db_session)
        existing_data = await repo.read_by("title", a_organization.title)
        assert existing_data
        assert existing_data.title == data["title"]


async def test_read_organization_by_id_as_superuser_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"organizations/{entry_id}",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ERROR_MESSAGE_ORGANIZATION_NOT_FOUND
