import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import ClientReportRepository
from app.models import ClientReport

pytestmark = pytest.mark.asyncio


async def test_client_report_repo_table(db_session: AsyncSession) -> None:
    repo: ClientReportRepository = ClientReportRepository(session=db_session)
    assert repo._table is ClientReport
