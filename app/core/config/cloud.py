from os import environ
from typing import Optional

from dotenv import load_dotenv
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class CloudKeySettings(BaseSettings):
    # IP Info
    ipinfo: Optional[str] = environ.get("CLOUDKEY_IPINFO", None)
    # Google Cloud
    googleapi: Optional[str] = environ.get("CLOUDKEY_GOOGLE_API", None)
    # AWS
    aws_access_key_id: str = environ.get("CLOUDKEY_AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = environ.get("CLOUDKEY_AWS_SECRET_ACCESS_KEY", "")
    aws_default_region: str = environ.get("CLOUDKEY_AWS_DEFAULT_REGION", "")
    aws_s3_default_bucket: str = environ.get("CLOUDKEY_AWS_S3_DEFAULT_BUCKET", "")

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="CLOUDKEY_",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("aws_access_key_id", mode="before")
    def validate_aws_access_key_id(
        cls, v: str, info: ValidationInfo
    ) -> str:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("AWS Access Key ID not set.")

    @field_validator("aws_secret_access_key", mode="before")
    def validate_aws_secret_access_key(
        cls, v: str, info: ValidationInfo
    ) -> str:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("AWS Secret Access Key not set.")

    @field_validator("aws_default_region", mode="before")
    def validate_aws_default_region(
        cls, v: str, info: ValidationInfo
    ) -> str:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("AWS Default Region not set.")

    @field_validator("aws_s3_default_bucket", mode="before")
    def validate_aws_s3_default_bucket(
        cls, v: str, info: ValidationInfo
    ) -> str:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("AWS S3 Default Bucket Name not set.")
