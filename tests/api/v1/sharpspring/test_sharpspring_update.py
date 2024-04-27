from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.sharpspring import create_random_sharpspring
from tests.utils.utils import random_lower_string

from app.api.exceptions import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.schemas import ClientRead, SharpspringRead, SharpspringUpdate

pytestmark = pytest.mark.asyncio


async def test_update_sharpspring_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: SharpspringRead = await create_random_sharpspring(
        db_session, client_id=a_client.id
    )
    api_key: str = random_lower_string(64)
    data: Dict[str, str] = {"api_key": api_key}
    response: Response = await client.patch(
        f"sharpspring/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert updated_entry["id"] == str(entry_a.id)
    assert updated_entry["api_key"] == api_key
    assert updated_entry["secret_key"] == entry_a.secret_key


async def test_update_sharpspring_as_superuser_client_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: SharpspringRead = await create_random_sharpspring(
        db_session, client_id=a_client.id
    )
    fake_client_id = get_uuid_str()
    api_key: str = random_lower_string(64)
    data: Dict[str, str] = {"api_key": api_key, "client_id": fake_client_id}
    response: Response = await client.patch(
        f"sharpspring/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert updated_entry["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_update_sharpspring_as_superuser_api_key_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: SharpspringRead = await create_random_sharpspring(
        db_session, client_id=a_client.id
    )
    api_key: str = ""
    data: Dict[str, str] = {"api_key": api_key}
    response: Response = await client.patch(
        f"sharpspring/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert updated_entry["detail"][0]["msg"] == "Value error, api_key is required"


async def test_update_sharpspring_as_superuser_api_key_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: SharpspringRead = await create_random_sharpspring(
        db_session, client_id=a_client.id
    )
    api_key: str = random_lower_string(1) * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
    data: Dict[str, str] = {"api_key": api_key}
    response: Response = await client.patch(
        f"sharpspring/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == f"Value error, api_key must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )


async def test_update_sharpspring_as_superuser_secret_key_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: SharpspringRead = await create_random_sharpspring(
        db_session, client_id=a_client.id
    )
    secret_key: str = random_lower_string(1) * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
    data: Dict[str, str] = {"secret_key": secret_key}
    response: Response = await client.patch(
        f"sharpspring/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == f"Value error, secret_key must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )


async def test_update_sharpspring_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: SharpspringRead = await create_random_sharpspring(
        db_session, client_id=a_client.id
    )
    entry_b: SharpspringRead = await create_random_sharpspring(
        db_session, client_id=a_client.id
    )
    new_secret_key: str = random_lower_string(64)
    update_dict = SharpspringUpdate(
        api_key=entry_b.api_key,
        secret_key=new_secret_key,
    )
    response: Response = await client.patch(
        f"sharpspring/{entry_a.id}",
        headers=admin_token_headers,
        json=update_dict.model_dump(),
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_entry["detail"] == ErrorCode.SHARPSPRING_EXISTS
