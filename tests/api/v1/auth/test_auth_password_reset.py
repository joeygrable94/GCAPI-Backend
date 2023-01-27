from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.email import fast_mail
from tests.utils.users import create_new_user
from tests.utils.utils import random_lower_string

from app.api.errors import ErrorCode
from app.core.config import settings
from app.db.schemas import UserRead
from app.db.schemas.user import UserAdmin
from app.security import AuthManager

pytestmark = pytest.mark.asyncio


async def test_auth_random_user_reset_password(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserAdmin
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
    a_user: UserAdmin
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
    a_user: UserAdmin
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
    a_user: UserAdmin
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
