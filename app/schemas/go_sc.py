from __future__ import annotations

from typing import Optional

from pydantic import UUID4

from app.db.validators import ValidateSchemaTitleOptional, ValidateSchemaTitleRequired
from app.schemas.base import BaseSchemaRead


# schemas
class GoSearchConsolePropertyBase(
    ValidateSchemaTitleRequired,
):
    title: str
    client_id: UUID4
    website_id: UUID4


class GoSearchConsolePropertyCreate(GoSearchConsolePropertyBase):
    pass


class GoSearchConsolePropertyUpdate(
    ValidateSchemaTitleOptional,
):
    title: Optional[str] = None
    client_id: Optional[UUID4] = None
    website_id: Optional[UUID4] = None


class GoSearchConsolePropertyRead(
    GoSearchConsolePropertyBase,
    BaseSchemaRead,
):
    id: UUID4
