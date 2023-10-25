from __future__ import annotations

from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_corpus_optional,
    validate_corpus_required,
    validate_rawtext_optional,
    validate_rawtext_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class WebsiteKeywordCorpusBase(BaseSchema):
    corpus: str
    rawtext: str
    website_id: UUID4
    page_id: UUID4

    _validate_corpus = field_validator("corpus", mode="before")(
        validate_corpus_required
    )
    _validate_rawtext = field_validator("rawtext", mode="before")(
        validate_rawtext_required
    )


class WebsiteKeywordCorpusCreate(WebsiteKeywordCorpusBase):
    pass


class WebsiteKeywordCorpusUpdate(BaseSchema):
    corpus: Optional[str] = None
    rawtext: Optional[str] = None
    website_id: Optional[UUID4] = None
    page_id: Optional[UUID4] = None

    _validate_corpus = field_validator("corpus", mode="before")(
        validate_corpus_optional
    )
    _validate_rawtext = field_validator("rawtext", mode="before")(
        validate_rawtext_optional
    )


class WebsiteKeywordCorpusRead(WebsiteKeywordCorpusBase, BaseSchemaRead):
    id: UUID4
