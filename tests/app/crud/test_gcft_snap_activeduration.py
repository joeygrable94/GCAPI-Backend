import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GcftSnapActivedurationRepository
from app.models import GcftSnapActiveduration

pytestmark = pytest.mark.asyncio


async def test_gcft_snap_activeduration_repo_table(db_session: AsyncSession) -> None:
    repo: GcftSnapActivedurationRepository = GcftSnapActivedurationRepository(
        session=db_session
    )
    assert repo._table is GcftSnapActiveduration
