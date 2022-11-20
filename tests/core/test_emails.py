import pytest

from app.core.config import settings
from app.core.utilities import (
    get_uuid_str,
    send_account_registered,
    send_account_updated,
    send_email_confirmation,
    send_email_reset_password,
    send_email_verification,
    send_test_email,
)
from tests.utils.email import fast_mail
from tests.utils.utils import random_email, random_lower_string

pytestmark = pytest.mark.anyio


async def test_send_test_email() -> None:
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        username: str = random_email()
        await send_test_email(username)
        assert len(outbox) == 1
        assert outbox[0]["to"] == username
        assert (
            outbox[0]["from"]
            == f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        )


async def test_send_email_verification() -> None:
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        username: str = random_email()
        test_token: str = "TOKEN" + random_lower_string()
        test_token_csrf: str = get_uuid_str()
        await send_email_verification(
            email_to=username,
            username=username,
            token=test_token,
            csrf=test_token_csrf,
        )
        assert len(outbox) == 1
        assert outbox[0]["to"] == username
        assert (
            outbox[0]["from"]
            == f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        )


async def test_send_email_confirmation() -> None:
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        username: str = random_email()
        await send_email_confirmation(
            email_to=username, username=username, password="••••••••"
        )
        assert len(outbox) == 1
        assert outbox[0]["to"] == username
        assert (
            outbox[0]["from"]
            == f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        )


async def test_send_account_registered() -> None:
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        username: str = random_email()
        await send_account_registered(
            email_to=username, username=username, password="••••••••"
        )
        assert len(outbox) == 1
        assert outbox[0]["to"] == username
        assert (
            outbox[0]["from"]
            == f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        )


async def test_send_account_updated() -> None:
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        username: str = random_email()
        await send_account_updated(
            email_to=username, username=username, password="••••••••"
        )
        assert len(outbox) == 1
        assert outbox[0]["to"] == username
        assert (
            outbox[0]["from"]
            == f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        )


async def test_send_email_reset_password() -> None:
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        username: str = random_email()
        test_token: str = "TOKEN" + random_lower_string()
        await send_email_reset_password(
            email_to=username, username=username, token=test_token
        )
        assert len(outbox) == 1
        assert outbox[0]["to"] == username
        assert (
            outbox[0]["from"]
            == f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        )
