from typing import Any, Dict

from httpx import AsyncClient, Headers, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings


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
