from typing import Optional

from pydantic import UUID4

from app.db.acls import ClientReportNoteACL
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class ClientReportNoteBase(BaseSchema):
    pass


class ClientReportNoteCreate(ClientReportNoteBase):
    client_report_id: UUID4
    note_id: UUID4


class ClientReportNoteUpdate(ClientReportNoteBase):
    client_report_id: Optional[UUID4]
    note_id: Optional[UUID4]


class ClientReportNoteRead(ClientReportNoteACL, ClientReportNoteBase, BaseSchemaRead):
    id: UUID4
