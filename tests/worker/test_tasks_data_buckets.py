import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.utils import random_lower_string

from app.crud import DataBucketRepository
from app.models import DataBucket
from app.schemas import ClientRead
from app.tasks import bg_task_create_client_data_bucket

pytestmark = pytest.mark.asyncio


async def test_worker_task_create_client_data_bucket(
    db_session: AsyncSession,
) -> None:
    client: ClientRead = await create_random_client(db_session)
    test_prefix = random_lower_string(16)
    await bg_task_create_client_data_bucket(
        bucket_prefix=test_prefix,
        client_id=str(client.id),
        bdx_feed_id=None,
        gcft_id=None,
    )
    data_repo = DataBucketRepository(db_session)
    data_bucket_in_db = await data_repo.exists_by_fields(
        {
            "bucket_prefix": test_prefix,
            "client_id": client.id,
        }
    )
    assert data_bucket_in_db is not None
    assert isinstance(data_bucket_in_db, DataBucket)


async def test_worker_task_create_client_data_bucket_duplcate_bucket(
    db_session: AsyncSession,
) -> None:
    client: ClientRead = await create_random_client(db_session)
    test_prefix = random_lower_string(16)
    await bg_task_create_client_data_bucket(
        bucket_prefix=test_prefix,
        client_id=str(client.id),
        bdx_feed_id=None,
        gcft_id=None,
    )
    await bg_task_create_client_data_bucket(
        bucket_prefix=test_prefix,
        client_id=str(client.id),
        bdx_feed_id=None,
        gcft_id=None,
    )
    data_repo = DataBucketRepository(db_session)
    data_bucket_in_db = await data_repo.exists_by_fields(
        {
            "bucket_prefix": test_prefix,
            "client_id": client.id,
        }
    )
    assert data_bucket_in_db is not None
    assert isinstance(data_bucket_in_db, DataBucket)
