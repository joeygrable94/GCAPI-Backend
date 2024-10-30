from typing import Annotated

from fastapi import Depends

from app.core.cloud.aws import S3Storage
from app.core.config import Settings, get_settings


def get_aws_s3_service(settings: Settings = Depends(get_settings)) -> S3Storage:
    return S3Storage(
        default_region=settings.cloud.aws_default_region,
        default_bucket=settings.cloud.aws_s3_default_bucket,
    )


LoadAwsS3StorageService = Annotated[S3Storage, Depends(get_aws_s3_service)]
