from __future__ import annotations

from typing import Optional

from pydantic import UUID4, validator

from app.db.acls import WebsiteKeywordCorpusACL
from app.schemas.base import BaseSchema, BaseSchemaRead


# validators
class ValidateKeywordCorpusRequired(BaseSchema):
    corpus: str

    @validator("corpus")
    def limits_corpus(cls, v: str) -> str:
        if len(v) <= 0:
            raise ValueError("corpus text is required")
        if len(v) > 50000:
            raise ValueError("corpus must contain less than 50000 characters")
        return v


class ValidateKeywordCorpusOptional(BaseSchema):
    corpus: Optional[str]

    @validator("corpus")
    def limits_corpus(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) > 50000:
            raise ValueError("corpus must contain less than 50000 characters")
        return v


class ValidateKeywordRawTextRequired(BaseSchema):
    rawtext: str

    @validator("rawtext")
    def limits_rawtext(cls, v: str) -> str:
        if len(v) <= 0:
            raise ValueError("rawtext text is required")
        if len(v) > 50000:
            raise ValueError("rawtext must contain less than 50000 characters")
        return v


class ValidateKeywordRawTextOptional(BaseSchema):
    rawtext: Optional[str]

    @validator("rawtext")
    def limits_rawtext(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) > 50000:
            raise ValueError("rawtext must contain less than 50000 characters")
        return v


# schemas
class WebsiteKeywordCorpusBase(
    ValidateKeywordCorpusRequired, ValidateKeywordRawTextRequired, BaseSchema
):
    corpus: str
    rawtext: str
    website_id: UUID4
    page_id: UUID4


class WebsiteKeywordCorpusCreate(WebsiteKeywordCorpusBase):
    pass


class WebsiteKeywordCorpusUpdate(
    ValidateKeywordCorpusOptional, ValidateKeywordRawTextOptional, BaseSchema
):
    corpus: Optional[str]
    rawtext: Optional[str]
    website_id: Optional[UUID4]
    page_id: Optional[UUID4]


class WebsiteKeywordCorpusRead(
    WebsiteKeywordCorpusACL, WebsiteKeywordCorpusBase, BaseSchemaRead
):
    id: UUID4
