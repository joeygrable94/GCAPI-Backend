from pydantic import UUID4, field_validator

from app.core.schema import BaseSchema, BaseSchemaRead
from app.db.validators import validate_change_type_required


class AuditLogBase(BaseSchema):
    change_type: str
    change_spec: dict
    user_id: UUID4
    ipaddress_id: UUID4

    _validate_change_type = field_validator("change_type", mode="before")(
        validate_change_type_required
    )


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogUpdate(BaseSchema):
    # logs are immutable
    pass


class AuditLogRead(AuditLogBase, BaseSchemaRead):
    id: UUID4
