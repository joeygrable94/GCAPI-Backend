from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .website import Website  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class WebsiteKeywordCorpus(Base):
    __tablename__: str = "website_keywordcorpus"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        index=True,
        nullable=False,
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
    corpus: Mapped[str] = mapped_column(Text, nullable=False, default="")
    rawtext: Mapped[str] = mapped_column(Text, nullable=False, default="")

    # relationships
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website.id"), nullable=False
    )
    page_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website_page.id"), nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"KeywordCorpus({self.id}, Site[{self.website_id}], Pg[{self.page_id}])"
        )
        return repr_str
