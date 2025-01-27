import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GcftSnapTrafficsourceRepository
from app.models import GcftSnapTrafficsource

pytestmark = pytest.mark.asyncio


async def test_gcft_snap_trafficsource_repo_table(db_session: AsyncSession) -> None:
    repo: GcftSnapTrafficsourceRepository = GcftSnapTrafficsourceRepository(
        session=db_session
    )
    assert repo._table is GcftSnapTrafficsource
