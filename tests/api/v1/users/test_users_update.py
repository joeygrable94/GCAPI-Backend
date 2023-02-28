from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.users import (
    create_new_user,
    create_random_user,
    get_current_user_tokens,
)
from tests.utils.utils import random_lower_string

from app.api.errors import ErrorCode
from app.core.config import settings
from app.db.schemas import UserUpdate
from app.db.schemas.user import UserPrincipals
from app.security import AuthManager

pytestmark = pytest.mark.asyncio


async def test_update_user_as_random_user_forbidden(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserPrincipals
    a_user_password: str
    a_user, a_user_password = await create_new_user(user_auth)
    b_user: UserPrincipals = await create_random_user(user_auth)
    update_dict = UserUpdate(
        password="NEWvalidPassw0rd",
        email=b_user.email,
    )
    a_user_access_header = await get_current_user_tokens(
        client, a_user.email, a_user_password
    )
    response: Response = await client.patch(
        f"users/{a_user.id}", headers=a_user_access_header, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 401
    assert updated_user["detail"]["code"] == 401
    assert updated_user["detail"]["reason"] == ErrorCode.TOKEN_INVALID


async def test_update_user_email_already_exists(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserPrincipals = await create_random_user(user_auth)
    b_user: UserPrincipals = await create_random_user(user_auth)
    data = {
        "password": "NEWvalidPassw0rd",
        "email": b_user.email,
    }
    response: Response = await client.patch(
        f"users/{a_user.id}", headers=superuser_token_headers, json=data
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_user["detail"] == ErrorCode.USER_ALREADY_EXISTS


async def test_update_user_email_too_short(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserPrincipals = await create_random_user(user_auth)
    fake_email: str = "a@g.c"
    data = {
        "password": "NEWvalidPassw0rd",
        "email": fake_email,
    }
    response: Response = await client.patch(
        f"users/{a_user.id}", headers=superuser_token_headers, json=data
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_user["detail"][0]["msg"] == "emails must contain 5 or more characters"
    )


async def test_update_user_email_invalid(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserPrincipals = await create_random_user(user_auth)
    fake_email: str = "a@gccx"
    data = {
        "password": "NEWvalidPassw0rd",
        "email": fake_email,
    }
    response: Response = await client.patch(
        f"users/{a_user.id}", headers=superuser_token_headers, json=data
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert updated_user["detail"][0]["msg"] == "value is not a valid email address"


async def test_update_user_email_invalid_provider(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserPrincipals = await create_random_user(user_auth)
    fake_email: str = "test@gmail.com"
    data = {
        "password": "NEWvalidPassw0rd",
        "email": fake_email,
    }
    response: Response = await client.patch(
        f"users/{a_user.id}", headers=superuser_token_headers, json=data
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert updated_user["detail"][0]["msg"] == "invalid email provider"


async def test_update_user_password_too_short(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserPrincipals = await create_random_user(user_auth)
    update_dict = UserUpdate(password="short")
    response: Response = await client.patch(
        f"users/{a_user.id}", headers=superuser_token_headers, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_user["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
    assert (
        updated_user["detail"]["reason"]
        == f"Password must contain {settings.PASSWORD_LENGTH_MIN} or more characters"
    )


async def test_update_user_password_too_long(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserPrincipals = await create_random_user(user_auth)
    new_pass: str = random_lower_string() * 10
    update_dict = UserUpdate(password=new_pass)
    response: Response = await client.patch(
        f"users/{a_user.id}", headers=superuser_token_headers, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_user["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
    assert (
        updated_user["detail"]["reason"]
        == f"Password must contain {settings.PASSWORD_LENGTH_MAX} or less characters"
    )
