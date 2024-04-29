from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.core.utilities.uuids import get_uuid_str
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.models import User
from app.schemas import ClientRead

pytestmark = pytest.mark.asyncio


async def test_create_bdx_feed_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    username: str = random_lower_string()
    password: str = random_lower_string()
    serverhost: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "username": username,
        "password": password,
        "serverhost": serverhost,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "bdx/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["username"] == username
    assert entry["password"] == password
    assert entry["serverhost"] == serverhost
    assert entry["client_id"] == str(a_client.id)


async def test_create_bdx_feed_as_superuser_client_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    fake_client_id = get_uuid_str()
    username: str = random_lower_string()
    password: str = random_lower_string()
    serverhost: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "username": username,
        "password": password,
        "serverhost": serverhost,
        "client_id": fake_client_id,
    }
    response: Response = await client.post(
        "bdx/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert entry["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_create_bdx_feed_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_user_a_client = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    username: str = random_lower_string()
    password: str = random_lower_string()
    serverhost: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "username": username,
        "password": password,
        "serverhost": serverhost,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "bdx/",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["username"] == username
    assert entry["password"] == password
    assert entry["client_id"] == str(a_client.id)


async def test_create_bdx_feed_as_employee_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    username: str = random_lower_string()
    password: str = random_lower_string()
    serverhost: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "username": username,
        "password": password,
        "serverhost": serverhost,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "bdx/",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert entry["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS


async def test_create_bdx_feed_as_superuser_bdx_feed_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    username: str = random_lower_string()
    password: str = random_lower_string()
    serverhost: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "username": username,
        "password": password,
        "serverhost": serverhost,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "bdx/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert entry["username"] == username
    assert entry["password"] == password
    assert entry["serverhost"] == serverhost
    assert entry["client_id"] == str(a_client.id)
    password_2: str = random_lower_string()
    data_in_2: Dict[str, Any] = {
        "username": username,
        "password": password_2,
        "serverhost": serverhost,
        "client_id": str(a_client.id),
    }
    response_2: Response = await client.post(
        "bdx/",
        headers=admin_token_headers,
        json=data_in_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ErrorCode.BDX_FEED_EXISTS


async def test_create_bdx_feed_as_superuser_bdx_feed_username_required(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    username: str = ""
    password: str = random_lower_string()
    serverhost: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "username": username,
        "password": password,
        "serverhost": serverhost,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "bdx/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert entry["detail"][0]["msg"] == "Value error, username is required"


async def test_create_bdx_feed_as_superuser_bdx_feed_username_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    username: str = "a"
    password: str = random_lower_string()
    serverhost: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "username": username,
        "password": password,
        "serverhost": serverhost,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "bdx/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, username must be {5} characters or more"
    )


async def test_create_bdx_feed_as_superuser_bdx_feed_username_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    username: str = "a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
    password: str = random_lower_string()
    serverhost: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "username": username,
        "password": password,
        "serverhost": serverhost,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "bdx/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, username must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )


async def test_create_bdx_feed_as_superuser_bdx_feed_password_required(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    username: str = random_lower_string()
    password: str = ""
    serverhost: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "username": username,
        "password": password,
        "serverhost": serverhost,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "bdx/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "Value error, password is required"


async def test_create_bdx_feed_as_superuser_bdx_feed_password_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    username: str = random_lower_string()
    password: str = "a"
    serverhost: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "username": username,
        "password": password,
        "serverhost": serverhost,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "bdx/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, password must be {5} characters or more"
    )  # noqa: E501


async def test_create_bdx_feed_as_superuser_bdx_feed_password_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    username: str = random_lower_string()
    password: str = "a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
    serverhost: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "username": username,
        "password": password,
        "serverhost": serverhost,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "bdx/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, password must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )


async def test_create_bdx_feed_as_superuser_bdx_feed_serverhost_required(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    username: str = random_lower_string()
    password: str = random_lower_string()
    serverhost: str = ""
    data_in: Dict[str, Any] = {
        "username": username,
        "password": password,
        "serverhost": serverhost,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "bdx/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "Value error, serverhost is required"


async def test_create_bdx_feed_as_superuser_bdx_feed_serverhost_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    username: str = random_lower_string()
    password: str = random_lower_string()
    serverhost: str = "a"
    data_in: Dict[str, Any] = {
        "username": username,
        "password": password,
        "serverhost": serverhost,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "bdx/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, serverhost must be {3} characters or more"
    )


async def test_create_bdx_feed_as_superuser_bdx_feed_serverhost_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    username: str = random_lower_string()
    password: str = random_lower_string()
    serverhost: str = "a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
    data_in: Dict[str, Any] = {
        "username": username,
        "password": password,
        "serverhost": serverhost,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "bdx/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, serverhost must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )
