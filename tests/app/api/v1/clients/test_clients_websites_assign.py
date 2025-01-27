from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import create_random_client
from tests.utils.websites import create_random_website

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
async def test_clients_assign_random_website_as_user(
    client_user: Any,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_website = await create_random_website(db_session)
    a_client = await create_random_client(db_session)
    client_website = {"client_id": str(a_client.id), "website_id": str(a_website.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/assign/website",
        headers=current_user.token_headers,
        json=client_website,
    )
    assert response.status_code == status_code
    data: dict[str, Any] = response.json()
    assert data["id"] is not None
    assert data["client_id"] == str(a_client.id)
    assert data["website_id"] == str(a_website.id)


@pytest.mark.parametrize(
    "client_user,by_key_id,error_msg",
    [
        (
            "admin_user",
            "website_id",
            ErrorCode.ENTITY_NOT_FOUND,
        ),
        (
            "manager_user",
            "website_id",
            ErrorCode.ENTITY_NOT_FOUND,
        ),
        ("admin_user", "client_id", ErrorCode.CLIENT_NOT_FOUND),
        ("manager_user", "client_id", ErrorCode.CLIENT_NOT_FOUND),
        pytest.param(
            "employee_user",
            "website_id",
            ErrorCode.ENTITY_NOT_FOUND,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACTION),
        ),
    ],
)
async def test_clients_assign_website_as_user_missmatching_website_id(
    client_user: Any,
    by_key_id: str,
    error_msg: str,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_website = await create_random_website(db_session)
    a_client = await create_random_client(db_session)
    a_bad_key_id = get_uuid_str()
    client_website: dict[str, str]
    if by_key_id == "website_id":
        client_website = {"website_id": a_bad_key_id, "client_id": str(a_client.id)}
    if by_key_id == "client_id":
        client_website = {"website_id": str(a_website.id), "client_id": a_bad_key_id}
    response: Response = await client.post(
        f"clients/{a_client.id}/assign/website",
        headers=current_user.token_headers,
        json=client_website,
    )
    assert response.status_code == 404
    data: dict[str, Any] = response.json()
    assert error_msg in data["detail"]
