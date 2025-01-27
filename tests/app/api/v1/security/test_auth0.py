from typing import Any

from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from tests.utils.auth0 import (
    get_auth0_access_token_value,
    get_invalid_token,
    get_malformed_token,
    get_missing_kid_token,
)


async def test_auth0_bearer_token_missing(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    response: Response = await client.get(
        "/users/me",
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Missing bearer token"


async def test_auth0_bad_bearer_token_malformed(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    admin_access_token = get_auth0_access_token_value(
        settings.auth.first_admin, settings.auth.first_admin_password
    )
    malformed_access_token = get_malformed_token(admin_access_token)
    response: Response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {malformed_access_token}"},
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token signature"


async def test_auth0_bad_bearer_token_missing_kid(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    admin_access_token = get_auth0_access_token_value(
        settings.auth.first_admin, settings.auth.first_admin_password
    )
    missing_kid_access_token = get_missing_kid_token(admin_access_token)
    response: Response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {missing_kid_access_token}"},
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Malformed token header"


async def test_auth0_bad_bearer_token_invalid_access(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    admin_access_token = get_auth0_access_token_value(
        settings.auth.first_admin, settings.auth.first_admin_password
    )
    invalid_access_token = get_invalid_token(admin_access_token)
    response: Response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {invalid_access_token}"},
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Malformed token"


async def test_auth0_valid_scope(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    admin_access_token = get_auth0_access_token_value(
        settings.auth.first_admin,
        settings.auth.first_admin_password,
        scopes="openid profile email access:test",
    )
    response: Response = await client.get(
        "/test-scope",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 200
    assert data["status"] == "ok"


async def test_auth0_invalid_scope(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    admin_access_token = get_auth0_access_token_value(
        settings.auth.first_admin, settings.auth.first_admin_password
    )
    response: Response = await client.get(
        "/test-scope",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 403
    assert data["detail"] == 'Missing "access:test" scope'
