from typing import Optional

from pydantic import UUID4

from app.db.schemas.base import BaseSchema, BaseSchemaRead


class WebsiteBase(BaseSchema):
    domain: str
    is_secure: bool = False


class WebsiteCreate(BaseSchema):
    domain: str
    is_secure: Optional[bool] = False


class WebsiteUpdate(BaseSchema):
    domain: Optional[str]
    is_secure: Optional[bool]


class WebsiteRead(WebsiteBase, BaseSchemaRead):
    id: UUID4
