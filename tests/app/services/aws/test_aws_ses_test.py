import unittest.mock

import pytest

from app.config import settings
from app.services.aws import S3Storage, SimpleEmailService, aws_settings


def test_ses_send_message_failed_to_send() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    ses = SimpleEmailService(
        default_region=aws_settings.aws_default_region,
        s3_storage=s3,
        allowed_from_emails=settings.email.allowed_from_emails,
    )
    subject = "Test Email"
    plain_text = "This is a test email."
    html_content = "<h1>This is a test email.</h1>"
    with unittest.mock.patch.object(
        ses.ses_client, "send_raw_email", return_value=None
    ) as mock_send_raw_email:
        mock_send_raw_email.return_value = unittest.mock.Mock()
        with pytest.raises(Exception) as error:
            email_content = ses.send_message(
                addr_from=settings.email.from_email,
                addr_to=[settings.email.test_user],
                addr_cc=[],
                subject=subject,
                message=plain_text,
                html_content=html_content,
            )
            assert email_content is None
            assert error.value == "Failed to send email."
