import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import FileAssetRepository
from app.models import FileAsset

pytestmark = pytest.mark.asyncio


async def test_file_asset_repo_table(db_session: AsyncSession) -> None:
    repo: FileAssetRepository = FileAssetRepository(session=db_session)
    assert repo._table is FileAsset
