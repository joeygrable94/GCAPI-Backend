from __future__ import annotations

from typing import Optional

from pydantic import UUID4, BaseModel, field_validator

from app.db.validators import validate_domain_optional, validate_domain_required
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class WebsiteBase(BaseSchema):
    domain: str
    is_secure: bool = False
    is_active: bool = True

    _validate_domain = field_validator("domain", mode="before")(
        validate_domain_required
    )


class WebsiteCreate(BaseSchema):
    domain: str
    is_secure: bool = False
    is_active: bool = True

    _validate_domain = field_validator("domain", mode="before")(
        validate_domain_required
    )


class WebsiteUpdate(BaseSchema):
    domain: Optional[str] = None
    is_secure: Optional[bool] = None
    is_active: Optional[bool] = None

    _validate_domain = field_validator("domain", mode="before")(
        validate_domain_optional
    )


class WebsiteRead(WebsiteBase, BaseSchemaRead):
    id: UUID4


# tasks
class WebsiteCreateProcessing(BaseModel):
    website: WebsiteRead
    task_id: UUID4
