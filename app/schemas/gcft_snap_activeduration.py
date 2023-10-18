from datetime import datetime

from pydantic import UUID4

from app.db.validators import ValidateSchemaActiveSecondsRequired
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GcftSnapActivedurationBase(ValidateSchemaActiveSecondsRequired):
    session_id: UUID4
    active_seconds: int
    visit_date: datetime
    gcft_id: UUID4
    snap_id: UUID4


class GcftSnapActivedurationCreate(GcftSnapActivedurationBase):
    pass


class GcftSnapActivedurationUpdate(BaseSchema):
    pass


class GcftSnapActivedurationRead(GcftSnapActivedurationBase, BaseSchemaRead):
    id: UUID4
