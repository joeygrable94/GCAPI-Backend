from typing import Annotated

from fastapi import Depends

from app.services.aws import AwsSettings, S3Storage, get_aws_settings


def get_aws_s3_service(settings: AwsSettings = Depends(get_aws_settings)) -> S3Storage:
    return S3Storage(
        default_region=settings.aws_default_region,
        default_bucket=settings.aws_s3_default_bucket,
    )


LoadAwsS3StorageService = Annotated[S3Storage, Depends(get_aws_s3_service)]
