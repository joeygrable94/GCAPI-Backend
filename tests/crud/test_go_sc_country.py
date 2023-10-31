import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GoSearchConsoleCountryRepository
from app.models import GoSearchConsoleCountry

pytestmark = pytest.mark.asyncio


async def test_go_sc_country_repo_table(db_session: AsyncSession) -> None:
    repo: GoSearchConsoleCountryRepository = GoSearchConsoleCountryRepository(
        session=db_session
    )
    assert repo._table is GoSearchConsoleCountry
