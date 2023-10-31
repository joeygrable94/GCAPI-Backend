import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import ClientBucketRepository
from app.models import ClientBucket

pytestmark = pytest.mark.asyncio


async def test_client_bucket_repo_table(db_session: AsyncSession) -> None:
    repo: ClientBucketRepository = ClientBucketRepository(session=db_session)
    assert repo._table is ClientBucket
