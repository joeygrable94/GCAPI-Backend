import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.gcft_snap_view.crud import GcftSnapViewRepository
from app.entities.gcft_snap_view.model import GcftSnapView

pytestmark = pytest.mark.anyio


async def test_gcft_snap_view_repo_table(db_session: AsyncSession) -> None:
    repo: GcftSnapViewRepository = GcftSnapViewRepository(session=db_session)
    assert repo._table is GcftSnapView
