from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.core.gcloud import GDRIVE_SCOPES, GoCloudDriveService, GoCloudServiceType


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
