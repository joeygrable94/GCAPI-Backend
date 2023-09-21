import pytest
from pydantic import EmailStr
from tests.utils.email import fast_mail
from tests.utils.utils import random_email

from app.core.config import settings
from app.core.utilities import send_test_email

pytestmark = pytest.mark.asyncio


async def test_send_test_email() -> None:
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        username: EmailStr = random_email()
        await send_test_email(username)
        assert len(outbox) == 1
        assert outbox[0]["to"] == username
        assert (
            outbox[0]["from"]
            == f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        )
