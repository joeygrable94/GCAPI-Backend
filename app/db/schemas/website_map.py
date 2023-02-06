from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4, validator

from app.db.acls.website_map import WebsiteMapACL
from app.db.schemas.base import BaseSchema, BaseSchemaRead


# validators
class ValidateWebsiteMapTitleRequired(BaseSchema):
    title: str

    @validator("title")
    def limits_title(cls, v: str) -> str:
        if len(v) < 5:
            raise ValueError("title must contain 5 or more characters")
        if len(v) > 255:
            raise ValueError("title must contain less than 255 characters")
        return v


class ValidateWebsiteMapTitleOptional(BaseSchema):
    title: Optional[str]

    @validator("title")
    def limits_title(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) < 5:
            raise ValueError("title must contain 5 or more characters")
        if v and len(v) > 255:
            raise ValueError("title must contain less than 255 characters")
        return v


class ValidateWebsiteMapFileNameRequired(BaseSchema):
    file_name: str

    @validator("file_name")
    def limits_file_name(cls, v: str) -> str:
        if len(v) < 5:
            raise ValueError("file name must contain 5 or more characters")
        if len(v) > 120:
            raise ValueError("file name must contain less than 120 characters")
        return v


class ValidateWebsiteMapFileNameOptional(BaseSchema):
    file_name: Optional[str]

    @validator("file_name")
    def limits_file_name(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) < 5:
            raise ValueError("file name must contain 5 or more characters")
        if v and len(v) > 120:
            raise ValueError("file name must contain less than 120 characters")
        return v


class ValidateWebsiteMapFilePathRequired(BaseSchema):
    file_path: str

    @validator("file_path")
    def limits_file_path(cls, v: str) -> str:
        if len(v) < 5:
            raise ValueError("file path must contain 5 or more characters")
        if len(v) > 255:
            raise ValueError("file path must contain less than 255 characters")
        return v


class ValidateWebsiteMapFilePathOptional(BaseSchema):
    file_path: Optional[str]

    @validator("file_path")
    def limits_file_path(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) < 5:
            raise ValueError("file path must contain 5 or more characters")
        if v and len(v) > 255:
            raise ValueError("file path must contain less than 255 characters")
        return v


# schemas
class WebsiteMapBase(BaseSchema):
    pass


class RequestWebsiteMapCreate(ValidateWebsiteMapTitleRequired, WebsiteMapBase):
    title: str
    website_id: UUID4


class WebsiteMapCreate(
    ValidateWebsiteMapFileNameRequired,
    ValidateWebsiteMapFilePathRequired,
    RequestWebsiteMapCreate,
    WebsiteMapBase,
):
    file_name: str
    file_path: str
    is_processed: bool = False


class WebsiteMapUpdate(
    ValidateWebsiteMapTitleOptional,
    WebsiteMapBase,
):
    title: Optional[str]
    is_processed: Optional[bool]


class WebsiteMapUpdateFile(
    ValidateWebsiteMapFileNameOptional,
    ValidateWebsiteMapFilePathOptional,
    WebsiteMapBase,
):
    file_name: Optional[str]
    file_path: Optional[str]


class WebsiteMapUpdateWebsiteId(WebsiteMapBase):
    website_id: Optional[UUID4]


class WebsiteMapRead(WebsiteMapACL, WebsiteMapCreate, WebsiteMapBase):
    id: UUID4


# relationships
class WebsiteMapReadRelations(WebsiteMapRead, BaseSchemaRead):
    pages: Optional[List["WebsitePageRead"]] = []


# import and update pydantic relationship refs
from app.db.schemas.website_page import WebsitePageRead  # noqa: E402

WebsiteMapReadRelations.update_forward_refs()
