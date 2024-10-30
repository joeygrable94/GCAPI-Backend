import pytest

from app.core.cloud.aws import S3Storage, SimpleEmailService
from app.core.config import settings

pytestmark = pytest.mark.asyncio


async def test_ses_class() -> None:
    s3 = S3Storage(
        default_region=settings.cloud.aws_default_region,
        default_bucket=settings.cloud.aws_s3_default_bucket,
    )
    ses = SimpleEmailService(
        default_region=settings.cloud.aws_default_region, s3_storage=s3
    )
    assert ses.region == settings.cloud.aws_default_region
