from datetime import datetime

from pydantic import UUID4, field_validator

from app.db.validators import validate_active_seconds_required
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GcftSnapActivedurationBase(BaseSchema):
    session_id: UUID4
    active_seconds: int
    visit_date: datetime
    gcft_id: UUID4
    snap_id: UUID4

    _validate_active_seconds = field_validator("active_seconds", mode="before")(
        validate_active_seconds_required
    )


class GcftSnapActivedurationCreate(GcftSnapActivedurationBase):
    pass


class GcftSnapActivedurationUpdate(BaseSchema):
    pass


class GcftSnapActivedurationRead(GcftSnapActivedurationBase, BaseSchemaRead):
    id: UUID4
