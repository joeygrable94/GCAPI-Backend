from __future__ import annotations

from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_project_id_required,
    validate_project_name_optional,
    validate_project_name_required,
    validate_project_number_required,
    validate_service_account_optional,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GoCloudPropertyBase(BaseSchema):
    project_name: str
    project_id: str
    project_number: str
    service_account: Optional[str] = None
    client_id: UUID4

    _validate_project_name = field_validator("project_name", mode="before")(
        validate_project_name_required
    )
    _validate_project_id = field_validator("project_id", mode="before")(
        validate_project_id_required
    )
    _validate_project_number = field_validator("project_number", mode="before")(
        validate_project_number_required
    )
    _validate_service_account = field_validator("service_account", mode="before")(
        validate_service_account_optional
    )


class GoCloudPropertyCreate(GoCloudPropertyBase):
    pass


class GoCloudPropertyUpdate(BaseSchema):
    project_name: Optional[str] = None
    service_account: Optional[str] = None
    client_id: Optional[UUID4] = None

    _validate_project_name = field_validator("project_name", mode="before")(
        validate_project_name_optional
    )
    _validate_service_account = field_validator("service_account", mode="before")(
        validate_service_account_optional
    )


class GoCloudPropertyRead(GoCloudPropertyBase, BaseSchemaRead):
    id: UUID4
