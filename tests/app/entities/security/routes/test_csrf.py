from hashlib import sha1
from os import urandom
from typing import Any

import pytest
from httpx import AsyncClient, Headers, Response
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.csrf import CsrfProtect, csrf_settings
from app.utilities import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser

pytestmark = pytest.mark.asyncio


async def test_get_csrf_token_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "/csrf",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    data_headers: Headers = response.headers
    csrf_from_data = data.get("csrf_token", None)
    csrf_from_header = data_headers.get(csrf_settings.csrf_header_key, None)
    assert 200 <= response.status_code < 300
    assert csrf_from_data is not None
    assert csrf_from_header is not None
    assert csrf_from_data == csrf_from_header


async def test_post_csrf_token_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "/csrf",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    data_headers: Headers = response.headers
    csrf_from_data = data.get("csrf_token", None)
    csrf_from_header = data_headers.get(csrf_settings.csrf_header_key, None)
    csrf_from_cookie = client.cookies.get(csrf_settings.csrf_name_key, "")
    assert 200 <= response.status_code < 300
    assert csrf_from_data is not None
    assert csrf_from_header is not None
    assert csrf_from_cookie is not None
    assert csrf_from_data == csrf_from_header
    assert csrf_from_cookie != csrf_from_header
    # use csrf token
    resp_headers = {
        csrf_settings.csrf_header_key: csrf_from_header,
    }
    client.cookies.set(csrf_settings.csrf_name_key, csrf_from_cookie)
    resp_headers.update(admin_user.token_headers)
    response_2: Response = await client.post(
        "/csrf",
        headers=resp_headers,
    )
    data_2: dict[str, Any] = response_2.json()
    data_2_headers: Headers = response_2.headers
    csrf_2_from_header = data_2_headers.get(csrf_settings.csrf_header_key, "")
    assert 200 <= response_2.status_code < 300
    assert data_2 is None
    assert csrf_2_from_header is not None
    assert len(csrf_2_from_header) == 0


async def test_post_csrf_token_as_admin_token_missing(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    # use csrf token
    resp_headers = {
        csrf_settings.csrf_header_key: get_uuid_str(),
    }
    client.cookies.clear()
    resp_headers.update(admin_user.token_headers)
    response_2: Response = await client.post(
        "/csrf",
        headers=resp_headers,
    )
    data_2: dict[str, Any] = response_2.json()
    assert response_2.status_code == 400
    assert data_2["detail"] == "Missing Cookie: `gcapi-csrf-token`."


async def test_post_csrf_token_as_admin_error_signature_mismatch(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "/csrf",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    data_headers: Headers = response.headers
    csrf_from_data = data.get("csrf_token", None)
    csrf_from_header = data_headers.get(csrf_settings.csrf_header_key, None)
    csrf_from_cookie = client.cookies.get(csrf_settings.csrf_name_key, "")
    assert 200 <= response.status_code < 300
    assert csrf_from_data is not None
    assert csrf_from_header is not None
    assert csrf_from_cookie is not None
    assert csrf_from_data == csrf_from_header
    assert csrf_from_cookie != csrf_from_header
    # use csrf token
    malformed_token = csrf_from_header + "malformed"
    resp_headers = {
        csrf_settings.csrf_header_key: malformed_token,
    }
    client.cookies.set(csrf_settings.csrf_name_key, csrf_from_cookie)
    resp_headers.update(admin_user.token_headers)
    response_2: Response = await client.post(
        "/csrf",
        headers=resp_headers,
    )
    data_2: dict[str, Any] = response_2.json()
    assert response_2.status_code == 401
    assert data_2["detail"] == "The CSRF signatures submitted do not match."


async def test_post_csrf_token_as_admin_error_bad_data(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "/csrf",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    data_headers: Headers = response.headers
    csrf_from_data = data.get("csrf_token", None)
    csrf_from_header = data_headers.get(csrf_settings.csrf_header_key, None)
    assert 200 <= response.status_code < 300
    assert csrf_from_data is not None
    assert csrf_from_header is not None
    assert csrf_from_data == csrf_from_header
    serializer = URLSafeTimedSerializer(csrf_settings.csrf_secret_key, salt="bad-salt")
    token = sha1(urandom(64)).hexdigest()
    signed_token = str(serializer.dumps(token))
    # use csrf token
    resp_headers = {
        csrf_settings.csrf_header_key: token,
    }
    client.cookies.set(csrf_settings.csrf_name_key, signed_token)
    resp_headers.update(admin_user.token_headers)
    response_2: Response = await client.post(
        "/csrf",
        headers=resp_headers,
    )
    data_2: dict[str, Any] = response_2.json()
    assert response_2.status_code == 401
    assert data_2["detail"] == "The CSRF token is invalid."


async def test_post_csrf_token_as_admin_invalid_headers(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "/csrf",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    data_headers: Headers = response.headers
    csrf_from_data = data.get("csrf_token", None)
    csrf_from_header = data_headers.get(csrf_settings.csrf_header_key, None)
    assert 200 <= response.status_code < 300
    assert csrf_from_data is not None
    assert csrf_from_header is not None
    assert csrf_from_data == csrf_from_header
    serializer = URLSafeTimedSerializer(
        csrf_settings.csrf_secret_key, salt=csrf_settings.csrf_salt
    )
    token = sha1(urandom(64)).hexdigest()
    signed_token = str(serializer.dumps(token))
    # use csrf token
    resp_headers = {
        "x-csrf-bad-header": token,
    }
    client.cookies.set(csrf_settings.csrf_name_key, signed_token)
    resp_headers.update(admin_user.token_headers)
    response_2: Response = await client.post(
        "/csrf",
        headers=resp_headers,
    )
    data_2: dict[str, Any] = response_2.json()
    assert response_2.status_code == 422
    assert data_2["detail"] == 'Bad headers. Expected "x-csrf-token" in headers'


async def test_post_csrf_token_as_admin_invalid_header_parts(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "/csrf",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    data_headers: Headers = response.headers
    csrf_from_data = data.get("csrf_token", None)
    csrf_from_header = data_headers.get(csrf_settings.csrf_header_key, None)
    assert 200 <= response.status_code < 300
    assert csrf_from_data is not None
    assert csrf_from_header is not None
    assert csrf_from_data == csrf_from_header
    serializer = URLSafeTimedSerializer(
        csrf_settings.csrf_secret_key, salt=csrf_settings.csrf_salt
    )
    token = sha1(urandom(64)).hexdigest()
    signed_token = str(serializer.dumps(token))
    # use csrf token
    resp_headers = {
        "x-csrf-token": "Bearer " + token,
    }
    client.cookies.set(csrf_settings.csrf_name_key, signed_token)
    resp_headers.update(admin_user.token_headers)
    response_2: Response = await client.post(
        "/csrf",
        headers=resp_headers,
    )
    data_2: dict[str, Any] = response_2.json()
    assert response_2.status_code == 422
    assert data_2["detail"] == 'Bad x-csrf-token header. Expected value "<Token>"'


async def test_post_csrf_token_as_admin_valid_header_parts_with_header_type(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    CsrfProtect._header_type = "Bearer"
    response: Response = await client.get(
        "/csrf",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    data_headers: Headers = response.headers
    csrf_from_data = data.get("csrf_token", None)
    csrf_from_header = data_headers.get(csrf_settings.csrf_header_key, None)
    assert 200 <= response.status_code < 300
    assert csrf_from_data is not None
    assert csrf_from_header is not None
    assert csrf_from_data == csrf_from_header
    serializer = URLSafeTimedSerializer(
        csrf_settings.csrf_secret_key, salt=csrf_settings.csrf_salt
    )
    token = sha1(urandom(64)).hexdigest()
    signed_token = str(serializer.dumps(token))
    # use csrf token
    resp_headers = {
        "x-csrf-token": "Bearer " + token,
    }
    client.cookies.set(csrf_settings.csrf_name_key, signed_token)
    resp_headers.update(admin_user.token_headers)
    response_2: Response = await client.post(
        "/csrf",
        headers=resp_headers,
    )
    data_2: dict[str, Any] = response_2.json()
    data_2_headers: Headers = response_2.headers
    csrf_2_from_header = data_2_headers.get(csrf_settings.csrf_header_key, "")
    assert 200 <= response_2.status_code < 300
    assert data_2 is None
    assert csrf_2_from_header is not None
    assert len(csrf_2_from_header) == 0
    # revert to original value
    CsrfProtect._header_type = None


async def test_post_csrf_token_as_admin_invalid_header_parts_with_header_type(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    CsrfProtect._header_type = "Bearer"
    response: Response = await client.get(
        "/csrf",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    data_headers: Headers = response.headers
    csrf_from_data = data.get("csrf_token", None)
    csrf_from_header = data_headers.get(csrf_settings.csrf_header_key, None)
    assert 200 <= response.status_code < 300
    assert csrf_from_data is not None
    assert csrf_from_header is not None
    assert csrf_from_data == csrf_from_header
    serializer = URLSafeTimedSerializer(
        csrf_settings.csrf_secret_key, salt=csrf_settings.csrf_salt
    )
    token = sha1(urandom(64)).hexdigest()
    signed_token = str(serializer.dumps(token))
    # use csrf token
    resp_headers = {
        "x-csrf-token": token,
    }
    client.cookies.set(csrf_settings.csrf_name_key, signed_token)
    resp_headers.update(admin_user.token_headers)
    response_2: Response = await client.post(
        "/csrf",
        headers=resp_headers,
    )
    data_2: dict[str, Any] = response_2.json()
    assert response_2.status_code == 422
    assert (
        data_2["detail"] == 'Bad x-csrf-token header. Expected value "Bearer <Token>"'
    )
    # revert to original value
    CsrfProtect._header_type = None
