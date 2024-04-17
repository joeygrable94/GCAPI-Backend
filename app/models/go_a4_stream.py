from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .go_a4 import GoAnalytics4Property  # noqa: F401


class GoAnalytics4Stream(Base):
    __tablename__: str = "go_a4_stream"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.current_timestamp(),
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    stream_id: Mapped[str] = mapped_column(
        String(16), nullable=False, unique=True, primary_key=True
    )

    # relationships
    ga4_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("go_a4.id"), nullable=False
    )
    ga4_account: Mapped["GoAnalytics4Property"] = relationship(
        "GoAnalytics4Property", back_populates="ga4_streams"
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"GoAnalytics4Stream({self.title} \
            Stream[{self.stream_id}] for GA4 Property[{self.ga4_id}])"
        )
        return repr_str
