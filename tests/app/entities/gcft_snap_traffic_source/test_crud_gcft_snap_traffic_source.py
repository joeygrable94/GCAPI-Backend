import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.gcft_snap_traffic_source.crud import GcftSnapTrafficsourceRepository
from app.entities.gcft_snap_traffic_source.model import GcftSnapTrafficsource

pytestmark = pytest.mark.anyio


async def test_gcft_snap_trafficsource_repo_table(db_session: AsyncSession) -> None:
    repo: GcftSnapTrafficsourceRepository = GcftSnapTrafficsourceRepository(
        session=db_session
    )
    assert repo._table is GcftSnapTrafficsource
