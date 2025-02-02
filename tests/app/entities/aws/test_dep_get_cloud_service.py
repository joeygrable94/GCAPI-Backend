from app.entities.aws.dependencies import get_aws_s3_service
from app.services.aws.service_s3 import S3Storage
from app.services.aws.settings import aws_settings


def test_get_aws_s3_service() -> None:
    service = get_aws_s3_service(aws_settings)
    check_service = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    assert service.default_bucket == check_service.default_bucket
    assert service.region == check_service.region
