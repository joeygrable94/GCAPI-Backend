from enum import Enum

from pydantic import BaseModel, EmailStr


class GoCloudServiceType(str, Enum):
    drive = "drive"


class GoCloudServiceVersion(str, Enum):
    drive = "v3"


class GoCloudDriveAssetsPage(BaseModel):
    success: bool
    results: list
    next_page_token: str | None


class GoCloudDriveAsset(BaseModel):
    success: bool
    asset: dict | None


class GoCloudDriveAssetId(BaseModel):
    success: bool
    asset_id: str | None


class GoCloudDriveSharedAsset(BaseModel):
    success: bool
    request_id: str
    asset_id: str
    email: EmailStr
