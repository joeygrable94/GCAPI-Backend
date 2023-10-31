import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GcftSnapRepository
from app.models import GcftSnap

pytestmark = pytest.mark.asyncio


async def test_gcft_snap_repo_table(db_session: AsyncSession) -> None:
    repo: GcftSnapRepository = GcftSnapRepository(session=db_session)
    assert repo._table is GcftSnap
