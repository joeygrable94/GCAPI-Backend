from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4

from app.db.validators import (
    ValidateSchemaDescriptionOptional,
    ValidateSchemaTitleOptional,
    ValidateSchemaTitleRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class NoteBase(ValidateSchemaTitleRequired, ValidateSchemaDescriptionOptional):
    title: str
    description: Optional[str] = None
    is_active: bool = True


class NoteCreate(NoteBase):
    title: str
    description: Optional[str] = None
    is_active: bool = True


class NoteUpdate(ValidateSchemaTitleOptional, ValidateSchemaDescriptionOptional):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class NoteRead(NoteBase, BaseSchemaRead):
    id: UUID4


# relationships
class NoteReadRelations(NoteRead):
    client_reports: Optional[List["ClientReportRead"]] = []


from app.schemas.client_report import ClientReportRead  # noqa: E402

NoteReadRelations.model_rebuild()
