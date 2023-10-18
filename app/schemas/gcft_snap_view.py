from datetime import datetime

from pydantic import UUID4

from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GcftSnapViewBase(BaseSchema):
    session_id: UUID4
    view_date: datetime
    gcft_id: UUID4
    snap_id: UUID4


class GcftSnapViewCreate(GcftSnapViewBase):
    pass


class GcftSnapViewUpdate(BaseSchema):
    pass


class GcftSnapViewRead(GcftSnapViewBase, BaseSchemaRead):
    id: UUID4
