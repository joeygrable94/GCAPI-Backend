from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4, BaseModel

from app.db.acls import WebsiteACL
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


class WebsiteRead(WebsiteACL, WebsiteBase, BaseSchemaRead):
    id: UUID4


# tasks
class WebsiteCreateProcessing(BaseModel):
    website: WebsiteRead
    task_id: UUID4


# relationships
class WebsiteReadRelations(WebsiteRead):
    clients: Optional[List["ClientRead"]] = []
    sitemaps: Optional[List["WebsiteMapRead"]] = []
    pages: Optional[List["WebsitePageRead"]] = []


# import and update pydantic relationship refs
from app.schemas.client import ClientRead  # noqa: E402
from app.schemas.website_map import WebsiteMapRead  # noqa: E402
from app.schemas.website_page import WebsitePageRead  # noqa: E402

WebsiteReadRelations.model_rebuild()
