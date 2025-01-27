import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GcftRepository
from app.models import Gcft

pytestmark = pytest.mark.asyncio


async def test_gcft_repo_table(db_session: AsyncSession) -> None:
    repo: GcftRepository = GcftRepository(session=db_session)
    assert repo._table is Gcft
