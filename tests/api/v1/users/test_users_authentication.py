from time import sleep
from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.core.config import settings
from app.core.redis import redis_conn
from app.core.utilities.uuids import get_uuid_str

pytestmark = pytest.mark.asyncio


async def test_login_current_user_admin(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    await redis_conn.flushall()
    csrf_response: Response = await client.get("users/request-auth")
    csrf_data: Dict[str, Any] = csrf_response.json()
    auth_request_token = csrf_data.get("auth_request_token")
    assert 200 <= csrf_response.status_code < 300
    csrf_from_header = csrf_response.headers.get(settings.api.csrf_header_key, "")
    auth_headers = {settings.api.csrf_header_key: csrf_from_header}
    login_data: Dict[str, Any] = dict(
        auth_request_token=auth_request_token,
        email=settings.auth.first_admin,
        password=settings.auth.first_admin_password,
        confirm_password=settings.auth.first_admin_password,
        auth_scope="",
    )
    sleep(1)
    response: Response = await client.post(
        "users/login",
        headers=auth_headers,
        json=login_data,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["token_type"] == "Bearer"
    assert len(data["access_token"]) > 0
    assert data["expires_in"] == 86400
    sleep(1)


async def test_login_current_user_passwords_mismatch(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    await redis_conn.flushall()
    csrf_response: Response = await client.get("users/request-auth")
    csrf_data: Dict[str, Any] = csrf_response.json()
    auth_request_token = csrf_data.get("auth_request_token")
    assert 200 <= csrf_response.status_code < 300
    csrf_from_header = csrf_response.headers.get(settings.api.csrf_header_key, "")
    auth_headers = {settings.api.csrf_header_key: csrf_from_header}
    login_data: Dict[str, Any] = dict(
        auth_request_token=auth_request_token,
        email=settings.auth.first_admin,
        password=settings.auth.first_admin_password,
        confirm_password=settings.auth.first_manager_password,
        auth_scope="",
    )
    sleep(1)
    response: Response = await client.post(
        "users/login",
        headers=auth_headers,
        json=login_data,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 401
    assert data["detail"] == ErrorCode.USER_PASSWORDS_MISMATCH
    sleep(1)


async def test_login_current_user_auth_request_pending(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    await redis_conn.flushall()
    csrf_response: Response = await client.get("users/request-auth")
    csrf_data: Dict[str, Any] = csrf_response.json()
    csrf_data.get("auth_request_token")
    assert 200 <= csrf_response.status_code < 300
    csrf_response_2: Response = await client.get("users/request-auth")
    csrf_data_2: Dict[str, Any] = csrf_response_2.json()
    assert csrf_response_2.status_code == 401
    assert csrf_data_2["detail"] == ErrorCode.USER_AUTH_REQUEST_PENDING


async def test_login_current_user_auth_request_requires_refresh(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    await redis_conn.flushall()
    auth_request_token = get_uuid_str()
    login_data: Dict[str, Any] = dict(
        auth_request_token=auth_request_token,
        email=settings.auth.first_admin,
        password=settings.auth.first_admin_password,
        confirm_password=settings.auth.first_manager_password,
        auth_scope="",
    )
    sleep(1)
    response: Response = await client.post(
        "users/login",
        json=login_data,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 401
    assert data["detail"] == ErrorCode.USER_AUTH_REQUEST_REFRESH_REQUIRED
    sleep(1)


async def test_login_current_user_auth_request_token_invalid(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    await redis_conn.flushall()
    csrf_response: Response = await client.get("users/request-auth")
    csrf_data: Dict[str, Any] = csrf_response.json()
    auth_request_token = csrf_data.get("auth_request_token")
    assert 200 <= csrf_response.status_code < 300
    csrf_from_header = csrf_response.headers.get(settings.api.csrf_header_key, "")
    assert auth_request_token == csrf_from_header
    auth_headers = {settings.api.csrf_header_key: csrf_from_header}
    invalid_auth_request_token = get_uuid_str()
    login_data: Dict[str, Any] = dict(
        auth_request_token=invalid_auth_request_token,
        email=settings.auth.first_admin,
        password=settings.auth.first_admin_password,
        confirm_password=settings.auth.first_admin_password,
        auth_scope="",
    )
    sleep(1)
    response: Response = await client.post(
        "users/login",
        headers=auth_headers,
        json=login_data,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 401
    assert data["detail"] == ErrorCode.USER_AUTH_REQUEST_INVALID_TOKEN
    sleep(1)
