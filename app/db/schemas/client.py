from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4, validator

from app.db.acls.client import ClientACL
from app.db.schemas.base import BaseSchema, BaseSchemaRead


# validators
class ValidateClientTitleRequired(BaseSchema):
    title: str

    @validator("title")
    def limits_title(cls, v: str) -> str:
        if len(v) < 5:
            raise ValueError("title must contain 5 or more characters")
        if len(v) > 96:
            raise ValueError("title must contain less than 96 characters")
        return v


class ValidateClientTitleOptional(BaseSchema):
    title: Optional[str]

    @validator("title")
    def limits_title(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) < 5:
            raise ValueError("title must contain 5 or more characters")
        if v and len(v) > 96:
            raise ValueError("title must contain less than 96 characters")
        return v


class ValidateClientContentOptional(BaseSchema):
    content: Optional[str]

    @validator("content")
    def limits_content(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) > 255:
            raise ValueError("content must contain less than 255 characters")
        return v


class ClientBase(ValidateClientTitleRequired, ValidateClientContentOptional):
    title: str
    content: Optional[str]


class ClientCreate(ClientBase):
    title: str
    content: Optional[str]


class ClientUpdate(ValidateClientTitleOptional, ValidateClientContentOptional):
    title: Optional[str]
    content: Optional[str]


class ClientRead(ClientACL, ClientBase, BaseSchemaRead):
    id: UUID4


# relationships
class ClientReadRelations(ClientRead):
    websites: Optional[List["WebsiteRead"]] = []
    # gcloud_accounts: Optional[List["GoogleCloudPropertyRead"]] = []
    # ga4_accounts: Optional[List["GoogleAnalytics4PropertyRead"]] = []
    # gua_accounts: Optional[List["GoogleUniversalAnalyticsPropertyRead"]] = []
    # sharpspring_accounts: Optional[List["SharpSpringRead"]] = []


# import and update pydantic relationship refs
from app.db.schemas.website import WebsiteRead  # noqa: E402

ClientReadRelations.update_forward_refs()
