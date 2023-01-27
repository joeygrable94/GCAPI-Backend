from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.email import fast_mail
from tests.utils.utils import random_email, random_lower_string

from app.api.errors import ErrorCode
from app.core.config import settings

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


async def test_auth_register_user_email_too_short(client: AsyncClient) -> None:
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        fake_email: str = "a@g.c"
        password: str = random_lower_string()
        data: Dict[str, str] = {
            "email": fake_email,
            "password": password,
        }
        response: Response = await client.post(
            "auth/register",
            json=data,
        )
        a_user: Dict[str, Any] = response.json()
        assert response.status_code == 422
        assert a_user["detail"][0]["msg"] == "emails must contain 5 or more characters"
        # check email verification
        assert len(outbox) == 0


async def test_auth_register_user_email_invalid(client: AsyncClient) -> None:
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        fake_email: str = "a@gccx"
        password: str = random_lower_string()
        data: Dict[str, str] = {
            "email": fake_email,
            "password": password,
        }
        response: Response = await client.post(
            "auth/register",
            json=data,
        )
        a_user: Dict[str, Any] = response.json()
        assert response.status_code == 422
        assert a_user["detail"][0]["msg"] == "value is not a valid email address"
        # check email verification
        assert len(outbox) == 0


async def test_auth_register_user_email_invalid_provider(client: AsyncClient) -> None:
    fast_mail.config.SUPPRESS_SEND = 1
    with fast_mail.record_messages() as outbox:
        fake_email: str = "test@gmail.com"
        password: str = random_lower_string()
        data: Dict[str, str] = {
            "email": fake_email,
            "password": password,
        }
        response: Response = await client.post(
            "auth/register",
            json=data,
        )
        a_user: Dict[str, Any] = response.json()
        assert response.status_code == 422
        assert a_user["detail"][0]["msg"] == "invalid email provider"
        # check email verification
        assert len(outbox) == 0


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
