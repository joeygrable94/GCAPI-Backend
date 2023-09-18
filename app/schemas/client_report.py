from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4

from app.db.acls import ClientReportACL
from app.db.validators import (
    ValidateSchemaDescriptionOptional,
    ValidateSchemaKeysOptional,
    ValidateSchemaTitleOptional,
    ValidateSchemaTitleRequired,
    ValidateSchemaUrlOptional,
    ValidateSchemaUrlRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class ClientReportBase(
    ValidateSchemaTitleRequired,
    ValidateSchemaUrlRequired,
    ValidateSchemaDescriptionOptional,
    ValidateSchemaKeysOptional,
):
    title: str
    url: str
    description: Optional[str]
    keys: Optional[str]
    client_id: UUID4


class ClientReportCreate(ClientReportBase):
    pass


class ClientReportUpdate(
    ValidateSchemaTitleOptional,
    ValidateSchemaUrlOptional,
    ValidateSchemaDescriptionOptional,
    ValidateSchemaKeysOptional,
):
    title: Optional[str]
    url: Optional[str]
    description: Optional[str]
    keys: Optional[str]
    client_id: Optional[UUID4]


class ClientReportRead(ClientReportACL, ClientReportBase, BaseSchemaRead):
    id: UUID4


# relationships
class ClientReportReadRelations(ClientReportRead):
    notes: Optional[List["NoteRead"]] = []


from app.schemas.note import NoteRead  # noqa: E402

ClientReportReadRelations.update_forward_refs()
