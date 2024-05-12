from app.api.utilities import create_or_read_data_bucket
from app.core.config import settings
from app.core.logger import logger
from app.worker import task_broker


@task_broker.task(task_name="datatask:task_create_client_data_bucket")
async def task_create_client_data_bucket(
    bucket_prefix: str,
    client_id: str,
    bdx_feed_id: str | None = None,
    gcft_id: str | None = None,
    bucket_name: str = settings.cloud.aws_s3_default_bucket,
) -> bool:
    success: bool = False
    try:
        data_bucket = await create_or_read_data_bucket(
            bucket_prefix=bucket_prefix,
            client_id=client_id,
            bdx_feed_id=bdx_feed_id,
            gcft_id=gcft_id,
            bucket_name=bucket_name,
        )
        if data_bucket is not None:
            success = True
    except Exception as e:  # pragma: no cover
        logger.warning("Error creating client data bucket")
        logger.warning(e)
        success = False
    finally:
        return success
