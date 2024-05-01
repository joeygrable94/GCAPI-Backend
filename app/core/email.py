from pathlib import Path

from fastapi_mail import ConnectionConfig  # type: ignore

from app.core.config import ApiModes, settings

email_conf: ConnectionConfig = ConnectionConfig(
    MAIL_USERNAME=settings.email.smtp_user,
    MAIL_PASSWORD=settings.email.smtp_password,
    MAIL_FROM=settings.email.from_email,
    MAIL_PORT=settings.email.smtp_port,
    MAIL_SERVER=settings.email.smtp_host,
    MAIL_FROM_NAME=settings.email.from_name,
    MAIL_STARTTLS=settings.email.smtp_tls,
    MAIL_SSL_TLS=settings.email.smtp_ssl,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER=Path(settings.email.templates_dir),
    SUPPRESS_SEND=1 if settings.api.mode == ApiModes.test else 0,
)
