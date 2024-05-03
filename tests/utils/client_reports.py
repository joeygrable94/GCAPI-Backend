from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_domain, random_lower_string

from app.crud import ClientReportNoteRepository, ClientReportRepository
from app.models import ClientReport, ClientReportNote
from app.schemas import (
    ClientReportCreate,
    ClientReportNoteCreate,
    ClientReportNoteRead,
    ClientReportRead,
)


async def create_random_client_report(
    db_session: AsyncSession, client_id: UUID4
) -> ClientReportRead:
    repo: ClientReportRepository = ClientReportRepository(session=db_session)
    client_report: ClientReport = await repo.create(
        schema=ClientReportCreate(
            title=random_lower_string(),
            url=f"{random_domain()}/{random_lower_string(6)}/{random_lower_string(6)}",
            description=random_lower_string(),
            keys=random_lower_string(),
            client_id=client_id,
        )
    )
    return ClientReportRead.model_validate(client_report)


async def create_random_client_report_note(
    db_session: AsyncSession, client_report_id: UUID4, note_id: UUID4
) -> ClientReportNoteRead:
    repo: ClientReportNoteRepository = ClientReportNoteRepository(session=db_session)
    client_report_note: ClientReportNote = await repo.create(
        schema=ClientReportNoteCreate(
            client_report_id=client_report_id,
            note_id=note_id,
        )
    )
    return ClientReportNoteRead.model_validate(client_report_note)
