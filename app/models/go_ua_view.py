from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .go_ua import GoogleUniversalAnalyticsProperty  # noqa: F401


class GoogleUniversalAnalyticsView(Base):
    __tablename__: str = "go_ua_view"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
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
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    view_id: Mapped[str] = mapped_column(String(16), nullable=False)

    # relationships
    gua_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("go_ua.id"), nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GoogleUniversalAnalyticsView({self.title} \
            View[{self.view_id}] for GUA Property[{self.gua_id}])"
        return repr_str
