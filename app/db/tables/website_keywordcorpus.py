from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.orm import Mapped

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .website import Website  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class WebsiteKeywordCorpus(TableBase):
    __tablename__: str = "website_keywordcorpus"
    corpus: Mapped[str] = Column(Text)
    rawtext: Mapped[str] = Column(Text)

    # relationships
    website_id: Mapped[UUID] = Column(GUID, ForeignKey("website.id"), nullable=False)
    page_id: Mapped[UUID] = Column(GUID, ForeignKey("website_page.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"KeywordCorpus({self.id}, Site[{self.website_id}], Pg[{self.page_id}])"
        )
        return repr_str