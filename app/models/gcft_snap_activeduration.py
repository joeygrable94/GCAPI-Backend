from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .gcft import GCFT  # noqa: F401
    from .gcft_snap import GCFTSnap  # noqa: F401


class GCFTSnapActiveDuration(Base):
    __tablename__: str = "gcft_snap_activeduration"
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
    session_id: Mapped[UUID4] = mapped_column(UUIDType(binary=False), nullable=False)
    active_seconds: Mapped[str] = mapped_column(Integer(), nullable=False)
    view_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    # relationships
    gcft_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft.id"), nullable=False
    )
    snap_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft_snap.id"), nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GCFTSnapActiveDuration({self.session_id} \
            on {self.view_date}, seconds={self.active_seconds})"
        return repr_str
