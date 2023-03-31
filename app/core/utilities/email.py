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
