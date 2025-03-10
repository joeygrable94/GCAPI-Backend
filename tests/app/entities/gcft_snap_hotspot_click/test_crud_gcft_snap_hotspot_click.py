import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.gcft_snap_hotspot_click.crud import GcftSnapHotspotclickRepository
from app.entities.gcft_snap_hotspot_click.model import GcftSnapHotspotclick

pytestmark = pytest.mark.anyio


async def test_gcft_snap_hotspotclick_repo_table(db_session: AsyncSession) -> None:
    repo: GcftSnapHotspotclickRepository = GcftSnapHotspotclickRepository(
        session=db_session
    )
    assert repo._table is GcftSnapHotspotclick
