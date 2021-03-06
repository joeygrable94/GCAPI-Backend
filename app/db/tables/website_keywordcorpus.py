from typing import TYPE_CHECKING

from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, ForeignKey, Text

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .website import Website  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class WebsiteKeywordCorpus(TableBase):
    __tablename__: str = "website_keywordcorpus"
    corpus = Column(Text)
    rawtext = Column(Text)

    # relationships
    website_id = Column(GUID, ForeignKey("website.id"), nullable=False)
    page_id = Column(GUID, ForeignKey("website_page.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str: str = (
            f"KeywordCorpus({self.id}, Site[{self.website_id}], Pg[{self.page_id}])"
        )
        return repr_str
