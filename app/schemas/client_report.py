from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4

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
    description: Optional[str] = None
    keys: Optional[str] = None
    client_id: UUID4


class ClientReportCreate(ClientReportBase):
    pass


class ClientReportUpdate(
    ValidateSchemaTitleOptional,
    ValidateSchemaUrlOptional,
    ValidateSchemaDescriptionOptional,
    ValidateSchemaKeysOptional,
):
    title: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    keys: Optional[str] = None
    client_id: Optional[UUID4] = None


class ClientReportRead(ClientReportBase, BaseSchemaRead):
    id: UUID4


# relationships
class ClientReportReadRelations(ClientReportRead):
    notes: Optional[List["NoteRead"]] = []


from app.schemas.note import NoteRead  # noqa: E402

ClientReportReadRelations.model_rebuild()
