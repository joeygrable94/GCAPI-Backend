from typing import Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.email import fast_mail
from tests.utils.users import create_random_user

from app.core.config import settings
from app.db.schemas.user import UserPrincipals
from app.security import AuthManager

pytestmark = pytest.mark.asyncio


async def test_auth_verify_random_user(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserPrincipals = await create_random_user(user_auth)
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
