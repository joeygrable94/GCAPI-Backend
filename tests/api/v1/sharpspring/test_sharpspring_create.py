from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.core.utilities import get_uuid_str
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.models import User
from app.schemas import ClientRead

pytestmark = pytest.mark.asyncio


async def test_create_sharpspring_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    api_key: str = random_lower_string()
    secret_key: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "api_key": api_key,
        "secret_key": secret_key,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "sharpspring/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["api_key"] == api_key
    assert entry["secret_key"] == secret_key
    assert entry["client_id"] == str(a_client.id)


async def test_create_sharpspring_as_superuser_client_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    fake_client_id = get_uuid_str()
    api_key: str = random_lower_string()
    secret_key: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "api_key": api_key,
        "secret_key": secret_key,
        "client_id": fake_client_id,
    }
    response: Response = await client.post(
        "sharpspring/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert entry["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_create_sharpspring_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_user_a_client = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    api_key: str = random_lower_string()
    secret_key: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "api_key": api_key,
        "secret_key": secret_key,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "sharpspring/",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["api_key"] == api_key
    assert entry["secret_key"] == secret_key
    assert entry["client_id"] == str(a_client.id)


async def test_create_sharpspring_as_employee_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    api_key: str = random_lower_string()
    secret_key: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "api_key": api_key,
        "secret_key": secret_key,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "sharpspring/",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert entry["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS


async def test_create_sharpspring_as_superuser_sharpspring_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    api_key: str = random_lower_string()
    secret_key: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "api_key": api_key,
        "secret_key": secret_key,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "sharpspring/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert entry["api_key"] == api_key
    assert entry["secret_key"] == secret_key
    assert entry["client_id"] == str(a_client.id)
    secret_key_2: str = random_lower_string()
    data_in_2: Dict[str, Any] = {
        "api_key": api_key,
        "secret_key": secret_key_2,
        "client_id": str(a_client.id),
    }
    response_2: Response = await client.post(
        "sharpspring/",
        headers=admin_token_headers,
        json=data_in_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ErrorCode.SHARPSPRING_EXISTS


async def test_create_sharpspring_as_superuser_sharpspring_api_key_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    api_key: str = ""
    secret_key: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "api_key": api_key,
        "secret_key": secret_key,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "sharpspring/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "Value error, api_key is required"


async def test_create_sharpspring_as_superuser_sharpspring_api_key_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    api_key: str = "a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
    secret_key: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "api_key": api_key,
        "secret_key": secret_key,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "sharpspring/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, api_key must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )


async def test_create_sharpspring_as_superuser_sharpspring_secret_key_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    api_key: str = random_lower_string()
    secret_key: str = ""
    data_in: Dict[str, Any] = {
        "api_key": api_key,
        "secret_key": secret_key,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "sharpspring/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "Value error, secret_key is required"


async def test_create_sharpspring_as_superuser_sharpspring_secret_key_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    api_key: str = random_lower_string()
    secret_key: str = "a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
    data_in: Dict[str, Any] = {
        "api_key": api_key,
        "secret_key": secret_key,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "sharpspring/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, secret_key must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )
