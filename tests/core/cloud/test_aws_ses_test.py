import unittest.mock

import pytest

from app.core.cloud.aws import S3Storage, SimpleEmailService
from app.core.config import settings


def test_ses_send_message_failed_to_send() -> None:
    s3 = S3Storage(
        default_region=settings.cloud.aws_default_region,
        default_bucket=settings.cloud.aws_s3_default_bucket,
    )
    ses = SimpleEmailService(
        default_region=settings.cloud.aws_default_region, s3_storage=s3
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
