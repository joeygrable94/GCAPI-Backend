from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import UUID4
from sqlalchemy import BLOB, DateTime, Float, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .go_sc import GoSearchConsoleProperty  # noqa: F401


class GoSearchConsoleQuery(Base):
    __tablename__: str = "go_sc_query"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        primary_key=True,
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
    keys: Mapped[str] = mapped_column(BLOB, nullable=False)
    clicks: Mapped[int] = mapped_column(Integer, nullable=False)
    impressions: Mapped[int] = mapped_column(Integer, nullable=False)
    ctr: Mapped[float] = mapped_column(Float(20), nullable=False)
    position: Mapped[float] = mapped_column(Float(20), nullable=False)
    date_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    date_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # relationships
    gsc_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("go_sc.id"), nullable=False
    )
    gsc_account: Mapped["GoSearchConsoleProperty"] = relationship(
        "GoSearchConsoleProperty", back_populates="gsc_queries"
    )

    # represenation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GoSearchConsoleQuery(GSCID[{self.gsc_id}], \
            C={self.clicks} I={self.impressions} CTR={self.ctr} Pos={self.position})"
        return repr_str
