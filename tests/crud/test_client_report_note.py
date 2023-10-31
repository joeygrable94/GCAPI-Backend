import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import ClientReportNoteRepository
from app.models import ClientReportNote

pytestmark = pytest.mark.asyncio


async def test_client_report_note_repo_table(db_session: AsyncSession) -> None:
    repo: ClientReportNoteRepository = ClientReportNoteRepository(session=db_session)
    assert repo._table is ClientReportNote
