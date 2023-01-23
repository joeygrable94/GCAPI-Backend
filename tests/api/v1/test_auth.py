from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.email import fast_mail
from tests.utils.users import (
    create_new_user,
    create_random_user,
    get_current_user_tokens,
)
from tests.utils.utils import random_email, random_lower_string

from app.api.errors import ErrorCode
from app.core.config import settings
from app.core.utilities import get_uuid_str
from app.db.schemas import UserCreate, UserRead
from app.db.schemas.user import UserReadAdmin
from app.db.tables.user import User
from app.security import AuthManager

pytestmark = pytest.mark.asyncio


async def test_auth_register_random_user(client: AsyncClient) -> None:
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        username: str = random_email()
        password: str = random_lower_string()
        data: Dict[str, str] = {"email": username, "password": password}
        response: Response = await client.post(
            "auth/register",
            json=data,
        )
        assert 200 <= response.status_code < 300
        a_user: Dict[str, Any] = response.json()
        assert "id" in a_user
        assert a_user["email"] == username
        assert "hashed_password" not in a_user
        assert "password" not in a_user
        assert a_user["is_active"]
        assert not a_user["is_verified"]
        assert not a_user["is_superuser"]
        # check email verification
        assert len(outbox) == 1
        assert (
            outbox[0]["from"]
            == f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        )
        assert outbox[0]["To"] == username
        assert (
            outbox[0]["Subject"]
            == f"{settings.PROJECT_NAME} - Email verification required"
        )


async def test_auth_register_user_already_exists(client: AsyncClient) -> None:
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        password: str = random_lower_string()
        data: Dict[str, str] = {
            "email": settings.TEST_NORMAL_USER,
            "password": password,
        }
        response: Response = await client.post(
            "auth/register",
            json=data,
        )
        assert response.status_code == 400
        a_user: Dict[str, Any] = response.json()
        assert a_user["detail"] == ErrorCode.USER_ALREADY_EXISTS
        # check email verification
        assert len(outbox) == 0


async def test_auth_register_user_password_too_long(client: AsyncClient) -> None:
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        username: str = random_email()
        password: str = random_lower_string() * 10
        data: Dict[str, str] = {"email": username, "password": password}
        response: Response = await client.post(
            "auth/register",
            json=data,
        )
        assert response.status_code == 400
        a_user: Dict[str, Any] = response.json()
        assert a_user["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
        assert (
            a_user["detail"]["reason"]
            == f"Password must contain {settings.PASSWORD_LENGTH_MAX} or less characters"  # noqa: E501
        )
        # check email verification
        assert len(outbox) == 0


async def test_auth_register_user_password_too_short(client: AsyncClient) -> None:
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        username: str = random_email()
        password: str = "1234567"
        data: Dict[str, str] = {"email": username, "password": password}
        response: Response = await client.post(
            "auth/register",
            json=data,
        )
        assert response.status_code == 400
        a_user: Dict[str, Any] = response.json()
        assert a_user["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
        assert (
            a_user["detail"]["reason"]
            == f"Password must contain {settings.PASSWORD_LENGTH_MIN} or more characters"  # noqa: E501
        )
        # check email verification
        assert len(outbox) == 0


async def test_auth_login_superuser(client: AsyncClient) -> None:
    response: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        },
    )
    tokens: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert "access_token_csrf" in tokens
    assert "refresh_token" in tokens
    assert "refresh_token_csrf" in tokens


async def test_auth_login_testuser(client: AsyncClient) -> None:
    response: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": settings.TEST_NORMAL_USER,
            "password": settings.TEST_NORMAL_USER_PASSWORD,
        },
    )
    tokens: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert "access_token_csrf" in tokens
    assert "refresh_token" in tokens
    assert "refresh_token_csrf" in tokens


async def test_auth_login_random_user(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserReadAdmin
    a_user_pass: str
    a_user, a_user_pass = await create_new_user(user_auth)
    response: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": a_user.email,
            "password": a_user_pass,
        },
    )
    tokens: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert "access_token_csrf" in tokens
    assert "refresh_token" in tokens
    assert "refresh_token_csrf" in tokens


async def test_auth_login_user_not_found(client: AsyncClient) -> None:
    not_username: str = random_email()
    password: str = random_lower_string()
    response: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": not_username,
            "password": password,
        },
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code >= 400
    assert "detail" in data
    assert data.get("detail") == ErrorCode.BAD_CREDENTIALS


async def test_auth_login_user_not_active(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    email: str = random_email()
    password: str = random_lower_string()
    a_user: User = await user_auth.users.create(
        schema=UserCreate(
            email=email,
            password=password,
            is_active=False,
            is_superuser=False,
            is_verified=False,
        )
    )
    response: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": a_user.email,
            "password": password,
        },
    )
    assert response.status_code >= 400
    data: Dict[str, Any] = response.json()
    assert "detail" in data
    assert data["detail"] == ErrorCode.USER_NOT_ACTIVE


async def test_auth_login_user_not_verified(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    settings.USERS_REQUIRE_VERIFICATION = True
    email: str = random_email()
    password: str = random_lower_string()
    a_user: User = await user_auth.users.create(
        schema=UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=False,
            is_verified=False,
        )
    )
    response: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": a_user.email,
            "password": password,
        },
    )
    assert response.status_code >= 400
    data: Dict[str, Any] = response.json()
    assert "detail" in data
    assert data["detail"] == ErrorCode.USER_NOT_VERIFIED


async def test_auth_logout_superuser_access(client: AsyncClient) -> None:
    super_user_tokens: Dict[str, str] = await get_current_user_tokens(client)
    a_tok: str = super_user_tokens["access_token"]
    access_headers: Dict[str, str] = {"Authorization": f"Bearer {a_tok}"}
    response: Response = await client.delete("auth/logout", headers=access_headers)
    data: Dict[str, str] = response.json()
    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"] == ""
    assert data["access_token_csrf"] == ""
    assert data["refresh_token"] == ""
    assert data["refresh_token_csrf"] == ""


async def test_auth_logout_testuser_access(client: AsyncClient) -> None:
    super_user_tokens: Dict[str, str] = await get_current_user_tokens(
        client, settings.TEST_NORMAL_USER, settings.TEST_NORMAL_USER_PASSWORD
    )
    a_tok: str = super_user_tokens["access_token"]
    access_headers: Dict[str, str] = {"Authorization": f"Bearer {a_tok}"}
    response: Response = await client.delete("auth/logout", headers=access_headers)
    data: Dict[str, str] = response.json()
    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"] == ""
    assert data["access_token_csrf"] == ""
    assert data["refresh_token"] == ""
    assert data["refresh_token_csrf"] == ""


async def test_auth_logout_random_user(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserReadAdmin
    a_user_pass: str
    a_user, a_user_pass = await create_new_user(user_auth)
    random_user_tokens: Dict[str, str] = await get_current_user_tokens(
        client, username=a_user.email, password=a_user_pass
    )
    a_tok: str = random_user_tokens["access_token"]
    access_headers: Dict[str, str] = {"Authorization": f"Bearer {a_tok}"}
    response: Response = await client.delete("auth/logout", headers=access_headers)
    data: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"] == ""
    assert data["access_token_csrf"] == ""
    assert data["refresh_token"] == ""
    assert data["refresh_token_csrf"] == ""


async def test_auth_refresh_superuser_access(client: AsyncClient) -> None:
    su_tokens: Dict[str, str] = await get_current_user_tokens(client)
    a_tok: str = su_tokens["access_token"]
    a_tok_csrf: str = su_tokens["access_token_csrf"]
    r_tok: str = su_tokens["refresh_token"]
    r_tok_csrf: str = su_tokens["refresh_token_csrf"]
    refresh_headers: Dict[str, str] = {"Authorization": f"Bearer {r_tok}"}
    response: Response = await client.post("auth/refresh", headers=refresh_headers)
    data: Dict[str, str] = response.json()
    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"] != ""
    assert data["access_token"] != a_tok
    assert data["access_token_csrf"] != a_tok_csrf
    assert data["refresh_token"] != ""
    assert data["refresh_token"] != r_tok
    assert data["refresh_token_csrf"] != r_tok_csrf


async def test_auth_revoke_superuser_access(client: AsyncClient) -> None:
    super_user_tokens: Dict[str, str] = await get_current_user_tokens(client)
    a_tok: str = super_user_tokens["access_token"]
    access_headers: Dict[str, str] = {"Authorization": f"Bearer {a_tok}"}
    response: Response = await client.delete("auth/revoke", headers=access_headers)
    data: Dict[str, str] = response.json()
    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"] == ""
    assert data["access_token_csrf"] == ""
    assert data["refresh_token"] == ""
    assert data["refresh_token_csrf"] == ""


async def test_auth_revoke_testuser_access(client: AsyncClient) -> None:
    test_user_tokens: Dict[str, str] = await get_current_user_tokens(
        client,
        username=settings.TEST_NORMAL_USER,
        password=settings.TEST_NORMAL_USER_PASSWORD,
    )
    a_tok: str = test_user_tokens["access_token"]
    access_headers: Dict[str, str] = {"Authorization": f"Bearer {a_tok}"}
    response: Response = await client.delete("auth/revoke", headers=access_headers)
    data: Dict[str, str] = response.json()
    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"] == ""
    assert data["access_token_csrf"] == ""
    assert data["refresh_token"] == ""
    assert data["refresh_token_csrf"] == ""


async def test_auth_verify_random_user(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserReadAdmin = await create_random_user(user_auth)
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        response: Response = await client.post(
            "auth/verification", json={"email": a_user.email}
        )
        data: Dict[str, str] = response.json()
        assert data is None
        # check email verification
        assert len(outbox) == 1
        assert (
            outbox[0]["from"]
            == f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        )
        assert outbox[0]["To"] == a_user.email
        assert (
            outbox[0]["Subject"]
            == f"{settings.PROJECT_NAME} - Email verification required"
        )


async def test_auth_verify_confirm_random_user(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserReadAdmin = await create_random_user(user_auth)
    a_tok: str
    a_tok_csrf: str
    a_tok, a_tok_csrf = await user_auth.store_token(
        user=a_user,
        audience=[settings.VERIFY_USER_TOKEN_AUDIENCE],
        expires=settings.VERIFY_USER_TOKEN_LIFETIME,
    )
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        response: Response = await client.get(
            f"auth/confirmation?token={a_tok}&csrf={a_tok_csrf}"
        )
        assert response.read() == b""
        assert response.status_code == 307
        test_next_url = response.next_request.url  # type: ignore
        assert test_next_url == f"http://{settings.SERVER_NAME}"
        # check email verification
        assert len(outbox) == 1
        assert (
            outbox[0]["from"]
            == f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        )
        assert outbox[0]["To"] == a_user.email
        assert outbox[0]["Subject"] == f"{settings.PROJECT_NAME} - User email verified"


async def test_auth_verify_confirm_random_user_bad_token(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserReadAdmin = await create_random_user(user_auth)  # noqa: F841
    a_tok: str = get_uuid_str()
    a_tok_csrf: str = get_uuid_str()
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        response: Response = await client.get(
            f"auth/confirmation?token={a_tok}&csrf={a_tok_csrf}"
        )
        data: Dict[str, Any] = response.json()
        assert response.status_code == 401
        assert data["detail"]["code"] == 401
        assert data["detail"]["reason"] == ErrorCode.TOKEN_INVALID
        # check email verification
        assert len(outbox) == 0


async def test_auth_verify_confirm_random_user_bad_csrf(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserReadAdmin = await create_random_user(user_auth)
    a_tok: str
    a_tok_csrf: str
    a_tok, a_tok_csrf = await user_auth.store_token(
        user=a_user,
        audience=[settings.VERIFY_USER_TOKEN_AUDIENCE],
        expires=settings.VERIFY_USER_TOKEN_LIFETIME,
    )
    b_tok_csrf: str = get_uuid_str()
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        response: Response = await client.get(
            f"auth/confirmation?token={a_tok}&csrf={b_tok_csrf}"
        )
        data: Dict[str, Any] = response.json()
        assert response.status_code == 401
        assert data["detail"]["code"] == 401
        assert data["detail"]["reason"] == ErrorCode.TOKEN_CSRF_INVALID
        # check email verification
        assert len(outbox) == 0


async def test_auth_random_user_forgot_password(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserReadAdmin = await create_random_user(user_auth)
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        response: Response = await client.post(
            "auth/forgot-password", json={"email": a_user.email}
        )
        data: Dict[str, str] = response.json()
        assert data is None
        # check email verification
        assert len(outbox) == 1
        assert (
            outbox[0]["from"]
            == f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        )
        assert outbox[0]["To"] == a_user.email
        assert (
            outbox[0]["Subject"]
            == f"{settings.PROJECT_NAME} - Password recovery for user {a_user.email}"
        )


async def test_auth_random_user_reset_password(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserReadAdmin
    a_user_pass: str
    a_user, a_user_pass = await create_new_user(user_auth)
    a_user_new_pass: str = random_lower_string()
    r_p_tok: str
    r_p_tok_csrf: str
    r_p_tok, r_p_tok_csrf = await user_auth.store_token(
        user=a_user,
        audience=[settings.RESET_PASSWORD_TOKEN_AUDIENCE],
        expires=settings.RESET_PASSWORD_TOKEN_LIFETIME,
    )
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        response: Response = await client.post(
            "auth/reset-password",
            json={"token": r_p_tok, "csrf": r_p_tok_csrf, "password": a_user_new_pass},
        )
        data: Dict[str, str] = response.json()
        assert data is not None
        user_data: UserRead = UserRead(**data)
        assert user_data.id == a_user.id
        # check email account updated
        assert len(outbox) == 1
        assert (
            outbox[0]["from"]
            == f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        )
        assert outbox[0]["To"] == a_user.email
        assert outbox[0]["Subject"] == f"{settings.PROJECT_NAME} - User account updated"


async def test_auth_unauthorized_user_reset_password(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserReadAdmin
    a_user_pass: str
    a_user, a_user_pass = await create_new_user(user_auth)
    a_user_new_pass: str = random_lower_string()
    r_p_tok: str
    r_p_tok_csrf: str
    r_p_tok, r_p_tok_csrf = await user_auth.store_token(
        user=a_user,
        audience=[settings.VERIFY_USER_TOKEN_AUDIENCE],
        expires=settings.RESET_PASSWORD_TOKEN_LIFETIME,
    )
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        response: Response = await client.post(
            "auth/reset-password",
            json={"token": r_p_tok, "csrf": r_p_tok_csrf, "password": a_user_new_pass},
        )
        data: Dict[str, Any] = response.json()
        assert data["detail"]["code"] == 401
        assert data["detail"]["reason"] == ErrorCode.TOKEN_INVALID
        # check no email sent
        assert len(outbox) == 0


async def test_auth_random_user_reset_password_too_long(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserReadAdmin
    a_user_pass: str
    a_user, a_user_pass = await create_new_user(user_auth)
    a_user_new_pass: str = random_lower_string() * 10
    r_p_tok: str
    r_p_tok_csrf: str
    r_p_tok, r_p_tok_csrf = await user_auth.store_token(
        user=a_user,
        audience=[settings.RESET_PASSWORD_TOKEN_AUDIENCE],
        expires=settings.RESET_PASSWORD_TOKEN_LIFETIME,
    )
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        response: Response = await client.post(
            "auth/reset-password",
            json={"token": r_p_tok, "csrf": r_p_tok_csrf, "password": a_user_new_pass},
        )
        assert response.status_code == 400
        data: Dict[str, Any] = response.json()
        assert data["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
        assert (
            data["detail"]["reason"]
            == f"Password must contain {settings.PASSWORD_LENGTH_MAX} or less characters"  # noqa: E501
        )
        # check email account updated
        assert len(outbox) == 0


async def test_auth_random_user_reset_password_too_short(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserReadAdmin
    a_user_pass: str
    a_user, a_user_pass = await create_new_user(user_auth)
    a_user_new_pass: str = "1234567"
    r_p_tok: str
    r_p_tok_csrf: str
    r_p_tok, r_p_tok_csrf = await user_auth.store_token(
        user=a_user,
        audience=[settings.RESET_PASSWORD_TOKEN_AUDIENCE],
        expires=settings.RESET_PASSWORD_TOKEN_LIFETIME,
    )
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        response: Response = await client.post(
            "auth/reset-password",
            json={"token": r_p_tok, "csrf": r_p_tok_csrf, "password": a_user_new_pass},
        )
        assert response.status_code == 400
        data: Dict[str, Any] = response.json()
        assert data["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
        assert (
            data["detail"]["reason"]
            == f"Password must contain {settings.PASSWORD_LENGTH_MIN} or more characters"  # noqa: E501
        )
        # check email verification
        assert len(outbox) == 0
