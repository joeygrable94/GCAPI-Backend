from typing import Any, Optional

from fastapi_mail import FastMail  # type: ignore
from fastapi_mail import MessageSchema

from app.core.config import settings
from app.core.email import email_conf
from app.core.logger import logger


async def _send_email(
    message: MessageSchema, template_name: Optional[str] = None
) -> Any:
    if settings.EMAILS_ENABLED and template_name is not None:
        try:
            fast_mail = FastMail(email_conf)
            await fast_mail.send_message(message, template_name=template_name)
            logger.info("sending email")
        except Exception as e:  # pragma: no cover
            logger.warning(e)


async def send_test_email(email_to: str) -> None:
    project_name: str = settings.PROJECT_NAME
    subject: str = f"{project_name} - Test email"
    message: MessageSchema = MessageSchema(
        subtype="html",
        subject=subject,
        recipients=[email_to],
        template_body={"project_name": project_name, "email": email_to},
    )
    await _send_email(message, template_name="test_email.html")


async def send_email_verification(
    email_to: str, username: str, token: str, csrf: str
) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Email verification required"
    server_host = f"{settings.SERVER_HOST}{settings.API_PREFIX_V1}"
    link = f"{server_host}/auth/confirmation?token={token}&csrf={csrf}"
    message: MessageSchema = MessageSchema(
        subtype="html",
        subject=subject,
        recipients=[email_to],
        template_body={
            "project_name": project_name,
            "username": username,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    await _send_email(message, template_name="email_verification.html")


async def send_email_confirmation(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - User email verified"
    link = settings.SERVER_HOST
    message: MessageSchema = MessageSchema(
        subtype="html",
        subject=subject,
        recipients=[email_to],
        template_body={
            "project_name": project_name,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )
    await _send_email(message, template_name="email_confirmation.html")


async def send_account_registered(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    link = settings.SERVER_HOST
    message: MessageSchema = MessageSchema(
        subtype="html",
        subject=subject,
        recipients=[email_to],
        template_body={
            "project_name": project_name,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )
    await _send_email(message, template_name="account_registered.html")


async def send_account_updated(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - User account updated"
    link = settings.SERVER_HOST
    message: MessageSchema = MessageSchema(
        subtype="html",
        subject=subject,
        recipients=[email_to],
        template_body={
            "project_name": project_name,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )
    await _send_email(message, template_name="account_updated.html")


async def send_email_reset_password(email_to: str, username: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {username}"
    server_host = f"{settings.SERVER_HOST}{settings.API_PREFIX_V1}"
    link = f"{server_host}/auth/reset-password?token={token}"
    message: MessageSchema = MessageSchema(
        subtype="html",
        subject=subject,
        recipients=[email_to],
        template_body={
            "project_name": project_name,
            "username": username,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    await _send_email(message, template_name="reset_password.html")
