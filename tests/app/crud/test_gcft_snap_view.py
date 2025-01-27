import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GcftSnapViewRepository
from app.models import GcftSnapView

pytestmark = pytest.mark.asyncio


async def test_gcft_snap_view_repo_table(db_session: AsyncSession) -> None:
    repo: GcftSnapViewRepository = GcftSnapViewRepository(session=db_session)
    assert repo._table is GcftSnapView
