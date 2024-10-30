from app.api.deps.get_cloud_service import get_aws_s3_service
from app.core.cloud.aws import S3Storage
from app.core.config import settings


def test_get_aws_s3_service() -> None:
    service = get_aws_s3_service(settings)
    check_service = S3Storage(
        default_region=settings.cloud.aws_default_region,
        default_bucket=settings.cloud.aws_s3_default_bucket,
    )
    assert service.default_bucket == check_service.default_bucket
    assert service.region == check_service.region
