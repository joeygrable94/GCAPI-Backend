from typing import Optional

from pydantic import UUID4

from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class ClientReportNoteBase(BaseSchema):
    client_report_id: UUID4
    note_id: UUID4


class ClientReportNoteCreate(ClientReportNoteBase):
    pass


class ClientReportNoteUpdate(BaseSchema):
    client_report_id: Optional[UUID4] = None
    note_id: Optional[UUID4] = None


class ClientReportNoteRead(ClientReportNoteBase, BaseSchemaRead):
    id: UUID4
