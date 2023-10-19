from __future__ import annotations

from typing import Optional

from pydantic import UUID4, BaseModel

from app.db.validators import ValidateSchemaDomainOptional, ValidateSchemaDomainRequired
from app.schemas.base import BaseSchemaRead


# schemas
class WebsiteBase(ValidateSchemaDomainRequired):
    domain: str
    is_secure: bool = False
    is_active: bool = True


class WebsiteCreate(ValidateSchemaDomainRequired):
    domain: str
    is_secure: bool = False
    is_active: bool = True


class WebsiteUpdate(ValidateSchemaDomainOptional):
    domain: Optional[str] = None
    is_secure: Optional[bool] = None
    is_active: Optional[bool] = None


class WebsiteRead(WebsiteBase, BaseSchemaRead):
    id: UUID4


# tasks
class WebsiteCreateProcessing(BaseModel):
    website: WebsiteRead
    task_id: UUID4
