import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import SharpspringRepository
from app.models import Sharpspring

pytestmark = pytest.mark.asyncio


async def test_sharpspring_repo_table(db_session: AsyncSession) -> None:
    repo: SharpspringRepository = SharpspringRepository(session=db_session)
    assert repo._table is Sharpspring
