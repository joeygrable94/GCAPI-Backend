from typing import Optional

from pydantic import UUID4

from app.db.acls import GoAnalytics4StreamACL
from app.db.validators import (
    ValidateSchemaStreamIdRequired,
    ValidateSchemaTitleOptional,
    ValidateSchemaTitleRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class GoAnalytics4StreamBase(
    ValidateSchemaTitleRequired,
    ValidateSchemaStreamIdRequired,
):
    title: str
    stream_id: str
    ga4_id: UUID4


class GoAnalytics4StreamCreate(GoAnalytics4StreamBase):
    pass


class GoAnalytics4StreamUpdate(
    ValidateSchemaTitleOptional,
):
    title: Optional[str]


class GoAnalytics4StreamRead(
    GoAnalytics4StreamACL,
    GoAnalytics4StreamBase,
    BaseSchemaRead,
):
    id: UUID4
