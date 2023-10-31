import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GoSearchConsolePropertyRepository
from app.models import GoSearchConsoleProperty

pytestmark = pytest.mark.asyncio


async def test_go_sc_repo_table(db_session: AsyncSession) -> None:
    repo: GoSearchConsolePropertyRepository = GoSearchConsolePropertyRepository(
        session=db_session
    )
    assert repo._table is GoSearchConsoleProperty
