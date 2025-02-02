from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import INT, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp, UUIDType

from app.db.base_class import Base
from app.utilities import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    from app.entities.gcft.model import Gcft
    from app.entities.gcft_snap.model import GcftSnap


class GcftSnapActiveduration(Base, Timestamp):
    __tablename__: str = "gcft_snap_activeduration"
    __table_args__: dict = {"mysql_engine": "InnoDB"}
    __mapper_args__: dict = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid,
    )
    session_id: Mapped[UUID4] = mapped_column(UUIDType(binary=False), nullable=False)
    active_seconds: Mapped[int] = mapped_column(INT, nullable=False)
    visit_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # relationships
    gcft_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft.id"), nullable=False
    )
    gcflytour: Mapped["Gcft"] = relationship("Gcft", back_populates="active_durations")
    snap_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft_snap.id"), nullable=False
    )
    gcft_snap: Mapped["GcftSnap"] = relationship(
        "GcftSnap", back_populates="active_durations"
    )

    # represenation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GcftSnapActiveduration({self.session_id} \
            on {self.visit_date}, seconds={self.active_seconds})"
        return repr_str
