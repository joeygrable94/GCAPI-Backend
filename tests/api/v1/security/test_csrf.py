from hashlib import sha1
from os import urandom
from typing import Any
from typing import Dict

from httpx import AsyncClient
from httpx import Headers
from httpx import Response
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.config import get_settings
from app.core.utilities.uuids import get_uuid_str


async def test_get_csrf_token_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    settings: Settings = get_settings()
    response: Response = await client.get(
        "/csrf",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    data_headers: Headers = response.headers
    csrf_from_data = data.get("csrf_token", None)
    csrf_from_header = data_headers.get(settings.api.csrf_header_key, None)
    csrf_from_cookie = client.cookies.get(settings.api.csrf_name_key, None)
    assert 200 <= response.status_code < 300
    assert csrf_from_data is not None
    assert csrf_from_header is not None
    assert csrf_from_data == csrf_from_header
    assert csrf_from_cookie != csrf_from_header


async def test_post_csrf_token_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    settings: Settings = get_settings()
    response: Response = await client.get(
        "/csrf",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    data_headers: Headers = response.headers
    csrf_from_data = data.get("csrf_token", None)
    csrf_from_header = data_headers.get(settings.api.csrf_header_key, None)
    csrf_from_cookie = client.cookies.get(settings.api.csrf_name_key, None)
    assert 200 <= response.status_code < 300
    assert csrf_from_data is not None
    assert csrf_from_header is not None
    assert csrf_from_cookie is not None
    assert csrf_from_data == csrf_from_header
    assert csrf_from_cookie != csrf_from_header
    # use csrf token
    resp_headers = {
        settings.api.csrf_header_key: csrf_from_header,
    }
    resp_headers.update(admin_token_headers)
    resp_cookies = {settings.api.csrf_name_key: csrf_from_cookie}
    response_2: Response = await client.post(
        "/csrf",
        headers=resp_headers,
        cookies=resp_cookies,
    )
    data_2: Dict[str, Any] = response_2.json()
    data_2_headers: Headers = response_2.headers
    csrf_2_from_header = data_2_headers.get(settings.api.csrf_header_key, "")
    csrf_2_from_cookie = client.cookies.get(settings.api.csrf_name_key, None)
    assert 200 <= response_2.status_code < 300
    assert data_2 is None
    assert csrf_2_from_cookie is None
    assert csrf_2_from_header is not None
    assert len(csrf_2_from_header) == 0


async def test_post_csrf_token_as_admin_token_missing(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    settings: Settings = get_settings()
    # use csrf token
    resp_headers = {
        settings.api.csrf_header_key: get_uuid_str(),
    }
    resp_headers.update(admin_token_headers)
    resp_cookies = {settings.api.csrf_name_key: None}
    response_2: Response = await client.post(
        "/csrf",
        headers=resp_headers,
        cookies=resp_cookies,  # type: ignore
    )
    data_2: Dict[str, Any] = response_2.json()
    assert response_2.status_code == 400
    assert data_2["detail"] == "Missing Cookie: `gcapi-csrf-token`."


async def test_post_csrf_token_as_admin_error_signature_mismatch(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    settings: Settings = get_settings()
    response: Response = await client.get(
        "/csrf",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    data_headers: Headers = response.headers
    csrf_from_data = data.get("csrf_token", None)
    csrf_from_header = data_headers.get(settings.api.csrf_header_key, None)
    csrf_from_cookie = client.cookies.get(settings.api.csrf_name_key, None)
    assert 200 <= response.status_code < 300
    assert csrf_from_data is not None
    assert csrf_from_header is not None
    assert csrf_from_cookie is not None
    assert csrf_from_data == csrf_from_header
    assert csrf_from_cookie != csrf_from_header
    # use csrf token
    malformed_token = csrf_from_header + "malformed"
    resp_headers = {
        settings.api.csrf_header_key: malformed_token,
    }
    resp_headers.update(admin_token_headers)
    resp_cookies = {settings.api.csrf_name_key: csrf_from_cookie}
    response_2: Response = await client.post(
        "/csrf",
        headers=resp_headers,
        cookies=resp_cookies,
    )
    data_2: Dict[str, Any] = response_2.json()
    assert response_2.status_code == 401
    assert data_2["detail"] == "The CSRF signatures submitted do not match."


async def test_post_csrf_token_as_admin_error_bad_data(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    settings: Settings = get_settings()
    response: Response = await client.get(
        "/csrf",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    data_headers: Headers = response.headers
    csrf_from_data = data.get("csrf_token", None)
    csrf_from_header = data_headers.get(settings.api.csrf_header_key, None)
    csrf_from_cookie = client.cookies.get(settings.api.csrf_name_key, None)
    assert 200 <= response.status_code < 300
    assert csrf_from_data is not None
    assert csrf_from_header is not None
    assert csrf_from_cookie is not None
    assert csrf_from_data == csrf_from_header
    assert csrf_from_cookie != csrf_from_header
    serializer = URLSafeTimedSerializer(settings.api.csrf_secret_key, salt="bad-salt")
    token = sha1(urandom(64)).hexdigest()
    signed_token = str(serializer.dumps(token))
    # use csrf token
    resp_headers = {
        settings.api.csrf_header_key: token,
    }
    resp_headers.update(admin_token_headers)
    resp_cookies = {settings.api.csrf_name_key: signed_token}
    response_2: Response = await client.post(
        "/csrf",
        headers=resp_headers,
        cookies=resp_cookies,
    )
    data_2: Dict[str, Any] = response_2.json()
    assert response_2.status_code == 401
    assert data_2["detail"] == "The CSRF token is invalid."


async def test_post_csrf_token_as_admin_invalid_header(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    settings: Settings = get_settings()
    response: Response = await client.get(
        "/csrf",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    data_headers: Headers = response.headers
    csrf_from_data = data.get("csrf_token", None)
    csrf_from_header = data_headers.get(settings.api.csrf_header_key, None)
    csrf_from_cookie = client.cookies.get(settings.api.csrf_name_key, None)
    assert 200 <= response.status_code < 300
    assert csrf_from_data is not None
    assert csrf_from_header is not None
    assert csrf_from_cookie is not None
    assert csrf_from_data == csrf_from_header
    assert csrf_from_cookie != csrf_from_header
    serializer = URLSafeTimedSerializer(
        settings.api.csrf_secret_key, salt=settings.api.csrf_salt
    )
    token = sha1(urandom(64)).hexdigest()
    signed_token = str(serializer.dumps(token))
    # use csrf token
    resp_headers = {
        "x-csrf-bad-header": token,
    }
    resp_headers.update(admin_token_headers)
    resp_cookies = {settings.api.csrf_name_key: signed_token}
    response_2: Response = await client.post(
        "/csrf",
        headers=resp_headers,
        cookies=resp_cookies,
    )
    data_2: Dict[str, Any] = response_2.json()
    assert response_2.status_code == 422
    assert data_2["detail"] == 'Bad headers. Expected "x-csrf-token" in headers'
