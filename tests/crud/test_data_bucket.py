import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import DataBucketRepository
from app.models import DataBucket

pytestmark = pytest.mark.asyncio


async def test_data_bucket_repo_table(db_session: AsyncSession) -> None:
    repo: DataBucketRepository = DataBucketRepository(session=db_session)
    assert repo._table is DataBucket
