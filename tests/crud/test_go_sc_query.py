import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GoSearchConsoleQueryRepository
from app.models import GoSearchConsoleQuery

pytestmark = pytest.mark.asyncio


async def test_go_sc_query_repo_table(db_session: AsyncSession) -> None:
    repo: GoSearchConsoleQueryRepository = GoSearchConsoleQueryRepository(
        session=db_session
    )
    assert repo._table is GoSearchConsoleQuery
