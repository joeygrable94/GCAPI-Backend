from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import Timestamp, UUIDType

from app.core.utilities import get_uuid
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .go_a4 import GoAnalytics4Property  # noqa: F401
    from .website import Website  # noqa: F401


class WebsiteGoAnalytics4Property(Base, Timestamp):
    __tablename__: str = "website_go_a4"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid,
    )
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("website.id"),
        primary_key=True,
        nullable=False,
    )
    go_a4_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("go_a4.id"),
        primary_key=True,
        nullable=False,
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"WebsiteGoAnalytics4Property({self.id}, [W({self.website_id}), GA4({self.go_a4_id})])"
        return repr_str
