import unittest.mock

import pytest

from app.config import settings
from app.services.aws import S3Storage, SimpleEmailService
from app.services.aws.settings import aws_settings


def test_ses_class() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    ses = SimpleEmailService(
        default_region=aws_settings.aws_default_region,
        s3_storage=s3,
        allowed_from_emails=settings.email.allowed_from_emails,
    )
    assert ses.region == aws_settings.aws_default_region
    assert ses.ses_client is not None
    assert isinstance(ses.s3_client, S3Storage)


def test_ses_create_message_data_plain_text() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    ses = SimpleEmailService(
        default_region=aws_settings.aws_default_region,
        s3_storage=s3,
        allowed_from_emails=settings.email.allowed_from_emails,
    )
    email_content = ses.create_message_data(
        sender=settings.email.from_email,
        to=[settings.email.test_user],
        cc=[],
        subject="Test Email",
        message_in="This is a test email.",
    )
    assert email_content is not None
    assert isinstance(email_content, str)
    assert "This is a test email." in email_content


def test_ses_create_message_data_html_content() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    ses = SimpleEmailService(
        default_region=aws_settings.aws_default_region,
        s3_storage=s3,
        allowed_from_emails=settings.email.allowed_from_emails,
    )
    plain_text = "This is a test email."
    html_content = "<h1>This is a test email.</h1>"
    email_content = ses.create_message_data(
        sender=settings.email.from_email,
        to=[settings.email.test_user],
        cc=[],
        subject="Test Email",
        message_in=plain_text,
        html_content=html_content,
    )
    assert email_content is not None
    assert isinstance(email_content, str)
    assert plain_text in email_content
    assert html_content in email_content


def test_ses_create_message_data_with_attachment() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    ses = SimpleEmailService(
        default_region=aws_settings.aws_default_region,
        s3_storage=s3,
        allowed_from_emails=settings.email.allowed_from_emails,
    )
    attatchment_object_key = "test.txt"
    attatchment_content = (
        f'Content-Disposition: attachment; filename="{attatchment_object_key}"'
    )
    plain_text = "This is a test email with an attachment."
    html_content = "<h1>This is a test email with an attachment.</h1>"
    email_content = ses.create_message_data(
        sender=settings.email.from_email,
        to=[settings.email.test_user],
        cc=[],
        subject="Test Email",
        message_in=plain_text,
        html_content=html_content,
        attatchments=[attatchment_object_key],
    )
    assert email_content is not None
    assert isinstance(email_content, str)
    assert plain_text in email_content
    assert html_content in email_content
    assert attatchment_content in email_content


def test_ses_create_message_data_with_attachment_not_found() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    ses = SimpleEmailService(
        default_region=aws_settings.aws_default_region,
        s3_storage=s3,
        allowed_from_emails=settings.email.allowed_from_emails,
    )
    attatchment_object_key = "test-not-found.txt"
    plain_text = "This is a test email with an attachment."
    html_content = "<h1>This is a test email with an attachment.</h1>"
    email_content = ses.create_message_data(
        sender=settings.email.from_email,
        to=[settings.email.test_user],
        cc=[],
        subject="Test Email",
        message_in=plain_text,
        html_content=html_content,
        attatchments=[attatchment_object_key],
    )
    assert email_content is None


def test_ses_send_message_from_unallowed_email() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    ses = SimpleEmailService(
        default_region=aws_settings.aws_default_region,
        s3_storage=s3,
        allowed_from_emails=settings.email.allowed_from_emails,
    )
    bad_from_email = "bademail@gmail.com"
    subject = "Test Email"
    plain_text = "This is a test email."
    html_content = "<h1>This is a test email.</h1>"
    with pytest.raises(Exception) as error:
        email_content = ses.send_message(
            addr_from=bad_from_email,
            addr_to=[settings.email.test_user],
            addr_cc=[],
            subject=subject,
            message=plain_text,
            html_content=html_content,
        )
        assert email_content is None
        assert error.value == f"Email({bad_from_email}) is not allowed to send emails."


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


def test_ses_send_message_success() -> None:
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
        ses.ses_client, "send_raw_email"
    ) as mock_send_raw_email:
        mock_send_raw_email.return_value = dict(MessageId="1234567890")
        email_content = ses.send_message(
            addr_from=settings.email.from_email,
            addr_to=[settings.email.test_user],
            addr_cc=[],
            subject=subject,
            message=plain_text,
            html_content=html_content,
        )
        assert email_content == "1234567890"
