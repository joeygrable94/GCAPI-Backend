from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.email import fast_mail
from tests.utils.users import create_random_user

from app.api.errors import ErrorCode
from app.core.config import settings
from app.core.utilities import get_uuid_str
from app.db.schemas.user import UserAdmin
from app.security import AuthManager

pytestmark = pytest.mark.asyncio


async def test_auth_verify_confirm_random_user(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
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
    a_user: UserAdmin = await create_random_user(user_auth)  # noqa: F841
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
    a_user: UserAdmin = await create_random_user(user_auth)
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
