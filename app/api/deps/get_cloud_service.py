from typing import Annotated

from fastapi import Depends

from app.core.cloud.aws import S3Storage
from app.core.cloud.google import GDRIVE_SCOPES, GoCloudDriveService, GoCloudServiceType
from app.core.config import Settings, get_settings


def get_go_cloud_gdrive_service(
    settings: Settings = Depends(get_settings),
) -> GoCloudDriveService:
    return GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
        service=GoCloudServiceType.drive,
        scopes=GDRIVE_SCOPES,
    )


LoadGoCloudDriveService = Annotated[
    GoCloudDriveService, Depends(get_go_cloud_gdrive_service)
]


def get_aws_s3_service(settings: Settings = Depends(get_settings)) -> S3Storage:
    return S3Storage(
        default_region=settings.cloud.aws_default_region,
        default_bucket=settings.cloud.aws_s3_default_bucket,
    )


LoadAwsS3StorageService = Annotated[S3Storage, Depends(get_aws_s3_service)]
