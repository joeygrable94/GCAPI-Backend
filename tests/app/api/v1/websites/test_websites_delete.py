from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.models import Website
from app.schemas import WebsiteRead
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user",
    [
        ("admin_user"),
        pytest.param(
            "manager_user",
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
    ],
)
async def test_delete_website_by_id_as_user(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    entry: Website | WebsiteRead = await create_random_website(db_session)
    response: Response = await client.delete(
        f"websites/{entry.id}",
        headers=current_user.token_headers,
    )
    assert 200 <= response.status_code < 300
    response: Response = await client.get(
        f"websites/{entry.id}",
        headers=current_user.token_headers,
    )
    assert response.status_code == 404
    data: dict[str, Any] = response.json()
    assert ErrorCode.ENTITY_NOT_FOUND in data["detail"]


@pytest.mark.parametrize(
    "client_user",
    [
        ("admin_user"),
        pytest.param(
            "manager_user",
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
    ],
)
async def test_delete_website_by_id_not_found(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    bad_website_id = get_uuid_str()
    response: Response = await client.delete(
        f"websites/{bad_website_id}",
        headers=current_user.token_headers,
    )
    assert response.status_code == 404
    data: dict[str, Any] = response.json()
    assert ErrorCode.ENTITY_NOT_FOUND in data["detail"]
