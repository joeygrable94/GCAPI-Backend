from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logger import logger
from app.core.utilities.uuids import parse_id
from app.crud import DataBucketRepository
from app.db.session import get_db_session
from app.models import DataBucket
from app.schemas import DataBucketCreate


async def create_or_read_data_bucket(
    bucket_prefix: str,
    client_id: str,
    bdx_feed_id: str | None,
    gcft_id: str | None,
    bucket_name: str = settings.cloud.aws_s3_default_bucket,
) -> DataBucket | None:
    try:
        client_uuid = parse_id(client_id)
        session: AsyncSession
        data_repo: DataBucketRepository
        data_bucket: DataBucket | None
        async with get_db_session() as session:
            data_repo = DataBucketRepository(session)
            data_bucket = await data_repo.exists_by_fields(
                {
                    "bucket_name": bucket_name,
                    "bucket_prefix": bucket_prefix,
                    "client_id": client_uuid,
                }
            )
            if data_bucket is None:
                data_bucket = await data_repo.create(
                    schema=DataBucketCreate(
                        bucket_name=bucket_name,
                        bucket_prefix=bucket_prefix,
                        client_id=client_uuid,
                        gcft_id=parse_id(gcft_id) if gcft_id else None,
                        bdx_feed_id=parse_id(bdx_feed_id) if bdx_feed_id else None,
                    )
                )
        return data_bucket
    except Exception as e:  # pragma: no cover
        logger.warning("Error fetching or creating Website Page: %s" % e)
        return None
