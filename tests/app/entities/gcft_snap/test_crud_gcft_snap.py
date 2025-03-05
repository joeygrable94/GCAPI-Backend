import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.gcft_snap.crud import GcftSnapRepository
from app.entities.gcft_snap.model import GcftSnap

pytestmark = pytest.mark.anyio


async def test_gcft_snap_repo_table(db_session: AsyncSession) -> None:
    repo: GcftSnapRepository = GcftSnapRepository(session=db_session)
    assert repo._table is GcftSnap
