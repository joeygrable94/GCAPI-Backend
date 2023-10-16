import pytest
from pydantic import EmailStr
from tests.utils.email import fast_mail
from tests.utils.utils import random_email

from app.core.config import settings
from app.core.utilities import send_test_email

pytestmark = pytest.mark.asyncio


async def test_send_test_email() -> None:
    with fast_mail.record_messages() as outbox:
        user_email: EmailStr = random_email()
        msg_sent: bool = await send_test_email(user_email)
        assert msg_sent
        assert len(outbox) == 1
        assert outbox[0]["to"] == user_email
        assert (
            outbox[0]["from"]
            == f"{settings.email.from_name} <{settings.email.from_email}>"
        )
