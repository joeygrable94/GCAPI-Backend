import pytest  # noqa

from app.api.deps import get_go_cloud_gdrive_service
from app.core.config import settings
from app.core.gcloud import GoCloudDriveService


def test_get_go_cloud_gdrive_service() -> None:
    service = get_go_cloud_gdrive_service(settings)
    assert isinstance(service, GoCloudDriveService)
