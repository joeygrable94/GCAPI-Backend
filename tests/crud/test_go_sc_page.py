import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GoSearchConsolePageRepository
from app.models import GoSearchConsolePage

pytestmark = pytest.mark.asyncio


async def test_go_sc_page_repo_table(db_session: AsyncSession) -> None:
    repo: GoSearchConsolePageRepository = GoSearchConsolePageRepository(
        session=db_session
    )
    assert repo._table is GoSearchConsolePage
