import json
from os import environ
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class CloudKeySettings(BaseSettings):
    # IP Info
    ipinfo: Optional[str] = environ.get("CLOUDKEY_IPINFO", None)
    # Google Cloud
    googleapi: Optional[str] = environ.get("CLOUDKEY_GOOGLE_API", None)
    googlecloudserviceaccount: dict[str, Any] = environ.get(  # type: ignore
        "CLOUDKEY_GOOGLE_CLOUD_SERVICE_ACCOUNT", ""
    )
    gocloud_default_delegated_account: str = environ.get(
        "CLOUDKEY_GOOGLE_CLOUD_DEFAULT_DELEGATED_ACCOUNT", ""
    )
    gocloud_gdrive_root_folder_id: str = environ.get(
        "CLOUDKEY_GDRIVE_ROOT_FOLDER_ID", ""
    )
    gocloud_gdrive_public_folder_id: str = environ.get(
        "CLOUDKEY_GDRIVE_PUBLIC_FOLDER_ID", ""
    )
    # AWS
    aws_access_key_id: str = environ.get("CLOUDKEY_AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = environ.get("CLOUDKEY_AWS_SECRET_ACCESS_KEY", "")
    aws_default_region: str = environ.get("CLOUDKEY_AWS_DEFAULT_REGION", "")
    aws_config_file: str = environ.get("CLOUDKEY_AWS_CONFIG_FILE", "~/.aws/config")
    aws_shared_credentials_file: str = environ.get(
        "CLOUDKEY_AWS_SHARED_CREDENTIALS_FILE", "~/.aws/credentials"
    )
    aws_s3_default_bucket: str = environ.get("CLOUDKEY_AWS_S3_DEFAULT_BUCKET", "")

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="CLOUDKEY_",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("googlecloudserviceaccount", mode="before")
    def validate_google_cloud_service_account(
        cls, v: str, info: ValidationInfo
    ) -> dict:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                data = json.loads(v, strict=False)
                return dict(data)
        raise ValueError("Google Cloud Service Account credentials are not set.")

    @field_validator("gocloud_default_delegated_account", mode="before")
    def validate_gocloud_default_delegated_account(
        cls, v: str, info: ValidationInfo
    ) -> str:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("Google Cloud default delegated account not set.")

    @field_validator("gocloud_gdrive_root_folder_id", mode="before")
    def validate_gocloud_gdrive_root_folder_id(
        cls, v: str, info: ValidationInfo
    ) -> str:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("Google Cloud Drive root folder id not set.")

    @field_validator("gocloud_gdrive_public_folder_id", mode="before")
    def validate_gocloud_gdrive_public_folder_id(
        cls, v: str, info: ValidationInfo
    ) -> str:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("Google Cloud Drive public folder id not set.")

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

    @field_validator("aws_config_file", mode="before")
    def validate_aws_config_file(
        cls, v: str, info: ValidationInfo
    ) -> str:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("AWS Config File path not set.")

    @field_validator("aws_shared_credentials_file", mode="before")
    def validate_aws_shared_credentials_file(
        cls, v: str, info: ValidationInfo
    ) -> str:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("AWS Shared Credentials File path not set.")

    @field_validator("aws_s3_default_bucket", mode="before")
    def validate_aws_s3_default_bucket(
        cls, v: str, info: ValidationInfo
    ) -> str:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("AWS S3 Default Bucket Name not set.")
