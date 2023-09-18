from typing import Type

from app.crud.base import BaseRepository
from app.models import ClientReportNote
from app.schemas import (
    ClientReportNoteCreate,
    ClientReportNoteRead,
    ClientReportNoteUpdate,
)


class ClientReportNoteRepository(
    BaseRepository[
        ClientReportNoteCreate,
        ClientReportNoteRead,
        ClientReportNoteUpdate,
        ClientReportNote,
    ]
):
    @property
    def _table(self) -> Type[ClientReportNote]:  # type: ignore
        return ClientReportNote
