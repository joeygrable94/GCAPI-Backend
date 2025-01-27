import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GcftSnapHotspotclickRepository
from app.models import GcftSnapHotspotclick

pytestmark = pytest.mark.asyncio


async def test_gcft_snap_hotspotclick_repo_table(db_session: AsyncSession) -> None:
    repo: GcftSnapHotspotclickRepository = GcftSnapHotspotclickRepository(
        session=db_session
    )
    assert repo._table is GcftSnapHotspotclick
