from __future__ import annotations

from typing import Optional

from pydantic import UUID4

from app.db.acls import WebsiteKeywordCorpusACL
from app.db.validators import (
    ValidateSchemaCorpusOptional,
    ValidateSchemaCorpusRequired,
    ValidateSchemaRawTextOptional,
    ValidateSchemaRawTextRequired,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class WebsiteKeywordCorpusBase(
    ValidateSchemaCorpusRequired, ValidateSchemaRawTextRequired, BaseSchema
):
    corpus: str
    rawtext: str
    website_id: UUID4
    page_id: UUID4


class WebsiteKeywordCorpusCreate(WebsiteKeywordCorpusBase):
    pass


class WebsiteKeywordCorpusUpdate(
    ValidateSchemaCorpusOptional, ValidateSchemaRawTextOptional, BaseSchema
):
    corpus: Optional[str]
    rawtext: Optional[str]
    website_id: Optional[UUID4]
    page_id: Optional[UUID4]


class WebsiteKeywordCorpusRead(
    WebsiteKeywordCorpusACL, WebsiteKeywordCorpusBase, BaseSchemaRead
):
    id: UUID4
