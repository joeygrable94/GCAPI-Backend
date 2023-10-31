import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GoSearchConsoleSearchappearanceRepository
from app.models import GoSearchConsoleSearchappearance

pytestmark = pytest.mark.asyncio


async def test_go_sc_searchappearance_repo_table(db_session: AsyncSession) -> None:
    repo: GoSearchConsoleSearchappearanceRepository = (
        GoSearchConsoleSearchappearanceRepository(session=db_session)
    )
    assert repo._table is GoSearchConsoleSearchappearance
