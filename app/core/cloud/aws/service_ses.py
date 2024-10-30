import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from boto3 import Session, client

from app.core import logger

from .service_s3 import S3Storage


class SimpleEmailService:
    def __init__(self, default_region: str, s3_storage: S3Storage) -> None:
        self.region: str = default_region
        self.session: Session = Session()
        self.ses_client = client("ses", region_name=default_region)
        self.s3_client = s3_storage

    def load_s3_file_attachment(
        self, object_key: str, bucket_name: str | None = None
    ) -> MIMEApplication | None:
        try:
            s3_bucket = (
                bucket_name
                if bucket_name is not None
                else self.s3_client.default_bucket
            )
            file_name = os.path.basename(object_key)
            if not self.s3_client.file_exists(object_key, s3_bucket):
                return None
            file_data = self.s3_client.read_file_bytes(object_key, s3_bucket)
            if file_data is None:  # pragma: no cover
                return None
            part = MIMEApplication(file_data)
            part.add_header("Content-Disposition", "attachment", filename=file_name)
            return part
        except Exception as e:  # pragma: no cover
            logger.warning("Error in load_s3_file_attachment()", e)
            return None

    def create_message_data(
        self,
        sender: str,
        to: list[str],
        cc: list[str],
        subject: str,
        message_in: str,
        html_content: str | None = None,
        attatchments: list[str] = [],
        bucket_name: str | None = None,
    ) -> str | None:
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = sender
            message["To"] = (", ").join(to)
            message["Cc"] = (", ").join(cc)
            # email body
            body_mime = MIMEText(message_in, "plain")
            message.attach(body_mime)
            if html_content:
                html_mime = MIMEText(html_content, "html")
                message.attach(html_mime)
            # email attachments
            for attachment in attatchments:
                part = self.load_s3_file_attachment(attachment, bucket_name)
                if part is not None:
                    message.attach(part)
            return message.as_string()
        except Exception as e:  # pragma: no cover
            logger.warning("Error in create_message()", e)
            return None

    def send_message(
        self,
        addr_from: str,
        addr_to: list[str],
        addr_cc: list[str] = [],
        subject: str = "AWS Email Subject",
        message: str = "Hello World",
        html_content: str | None = "<body><h1>Hello World</h1></body>",
        attatchments: list[str] = [],
    ) -> str | None:
        try:
            email_msg_bytes = self.create_message_data(
                sender=addr_from,
                to=addr_to,
                cc=addr_cc,
                subject=subject,
                message_in=message,
                html_content=html_content,
                attatchments=attatchments,
            )
            response = self.ses_client.send_raw_email(
                Source=addr_from,
                Destinations=addr_to,
                RawMessage={"Data": email_msg_bytes},
            )
            if "MessageId" in response:
                return response["MessageId"]
            else:  # pragma: no cover
                raise Exception("Failed to send email.")
        except Exception as e:  # pragma: no cover
            logger.warning("An error occurred: %s" % e)
            return None
