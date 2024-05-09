import json
from os import environ
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class CloudKeySettings(BaseSettings):
    googleapi: Optional[str] = environ.get("CLOUDKEY_GOOGLE_API", None)
    ipinfo: Optional[str] = environ.get("CLOUDKEY_IPINFO", None)
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
