from fastapi_mail import FastMail  # type: ignore

from app.core.email import email_conf

fast_mail = FastMail(email_conf)
