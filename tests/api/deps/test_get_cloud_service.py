import pytest  # noqa

from app.api.deps import get_aws_s3_service, get_go_cloud_gdrive_service
from app.core.cloud.aws import S3Storage
from app.core.cloud.google import GoCloudDriveService
from app.core.config import settings


def test_get_go_cloud_gdrive_service() -> None:
    service = get_go_cloud_gdrive_service(settings)
    assert isinstance(service, GoCloudDriveService)


def test_get_aws_s3_service() -> None:
    service = get_aws_s3_service(settings)
    assert isinstance(service, S3Storage)
