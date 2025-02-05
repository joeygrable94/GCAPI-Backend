import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import create_random_organization

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,item_count",
    [
        ("admin_user", 4),
        ("manager_user", 4),
        ("employee_user", 1),
    ],
)
async def test_list_all_organizations_as_user(
    client_user: dict[str, str],
    item_count: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    await create_random_organization(db_session)
    await create_random_organization(db_session)
    response: Response = await client.get(
        "organizations/", headers=current_user.token_headers
    )
    assert 200 <= response.status_code < 300
    data = response.json()
    assert data["page"] == 1
    assert data["total"] == item_count
    assert data["size"] == 1000
    assert len(data["results"]) == item_count
