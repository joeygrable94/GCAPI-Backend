from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.bdx_feed import create_random_bdx_feed
from tests.utils.clients import create_random_client
from tests.utils.utils import random_lower_string

from app.api.exceptions import ErrorCode
from app.core.utilities import get_uuid_str
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.schemas import BdxFeedRead, ClientRead

pytestmark = pytest.mark.asyncio


async def test_update_bdx_feed_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: BdxFeedRead = await create_random_bdx_feed(
        db_session, client_id=a_client.id
    )
    data: Dict[str, str] = {
        "username": entry_a.username,
        "serverhost": entry_a.serverhost,
    }
    response: Response = await client.patch(
        f"bdx/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_entry["detail"] == ErrorCode.BDX_FEED_EXISTS


async def test_update_bdx_feed_as_superuser_client_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: BdxFeedRead = await create_random_bdx_feed(
        db_session, client_id=a_client.id
    )
    fake_client_id = get_uuid_str()
    data: Dict[str, str] = {"username": entry_a.username, "client_id": fake_client_id}
    response: Response = await client.patch(
        f"bdx/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert updated_entry["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_update_bdx_feed_as_superuser_update_username(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: BdxFeedRead = await create_random_bdx_feed(
        db_session, client_id=a_client.id
    )
    username: str = random_lower_string(64)
    data: Dict[str, str] = {"username": username}
    response: Response = await client.patch(
        f"bdx/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert updated_entry["id"] == str(entry_a.id)
    assert updated_entry["username"] == username
    assert updated_entry["password"] == entry_a.password
    assert updated_entry["serverhost"] == entry_a.serverhost


async def test_update_bdx_feed_as_superuser_update_serverhost(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: BdxFeedRead = await create_random_bdx_feed(
        db_session, client_id=a_client.id
    )
    serverhost: str = random_lower_string(64)
    data: Dict[str, str] = {"serverhost": serverhost}
    response: Response = await client.patch(
        f"bdx/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert updated_entry["id"] == str(entry_a.id)
    assert updated_entry["username"] == entry_a.username
    assert updated_entry["password"] == entry_a.password
    assert updated_entry["serverhost"] == serverhost


async def test_update_bdx_feed_as_superuser_update_password(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: BdxFeedRead = await create_random_bdx_feed(
        db_session, client_id=a_client.id
    )
    password: str = random_lower_string(64)
    data: Dict[str, str] = {"password": password}
    response: Response = await client.patch(
        f"bdx/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert updated_entry["id"] == str(entry_a.id)
    assert updated_entry["username"] == entry_a.username
    assert updated_entry["password"] == password
    assert updated_entry["serverhost"] == entry_a.serverhost


async def test_update_bdx_feed_as_superuser_username_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: BdxFeedRead = await create_random_bdx_feed(
        db_session, client_id=a_client.id
    )
    username: str = "a"
    data: Dict[str, str] = {"username": username}
    response: Response = await client.patch(
        f"bdx/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == f"Value error, username must be {5} characters or more"
    )


async def test_update_bdx_feed_as_superuser_username_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: BdxFeedRead = await create_random_bdx_feed(
        db_session, client_id=a_client.id
    )
    username: str = random_lower_string(1) * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
    data: Dict[str, str] = {"username": username}
    response: Response = await client.patch(
        f"bdx/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == f"Value error, username must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )


async def test_update_bdx_feed_as_superuser_password_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: BdxFeedRead = await create_random_bdx_feed(
        db_session, client_id=a_client.id
    )
    password: str = "a"
    data: Dict[str, str] = {"password": password}
    response: Response = await client.patch(
        f"bdx/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == f"Value error, password must be {5} characters or more"
    )


async def test_update_bdx_feed_as_superuser_password_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: BdxFeedRead = await create_random_bdx_feed(
        db_session, client_id=a_client.id
    )
    password: str = random_lower_string(1) * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
    data: Dict[str, str] = {"password": password}
    response: Response = await client.patch(
        f"bdx/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == f"Value error, password must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )


async def test_update_bdx_feed_as_superuser_serverhost_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: BdxFeedRead = await create_random_bdx_feed(
        db_session, client_id=a_client.id
    )
    serverhost: str = "a"
    data: Dict[str, str] = {"serverhost": serverhost}
    response: Response = await client.patch(
        f"bdx/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == f"Value error, serverhost must be {3} characters or more"
    )


async def test_update_bdx_feed_as_superuser_serverhost_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: BdxFeedRead = await create_random_bdx_feed(
        db_session, client_id=a_client.id
    )
    serverhost: str = random_lower_string(1) * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
    data: Dict[str, str] = {"serverhost": serverhost}
    response: Response = await client.patch(
        f"bdx/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == f"Value error, serverhost must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )
