from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .gcft import Gcft  # noqa: F401
    from .gcft_snap import GcftSnap  # noqa: F401


class GcftSnapTrafficsource(Base):
    __tablename__: str = "gcft_snap_trafficsource"
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
    session_id: Mapped[UUID4] = mapped_column(UUIDType(binary=False), nullable=False)
    referrer: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
        default="/",
    )
    utm_campaign: Mapped[str] = mapped_column(String(255), nullable=True)
    utm_content: Mapped[str] = mapped_column(String(255), nullable=True)
    utm_medium: Mapped[str] = mapped_column(String(255), nullable=True)
    utm_source: Mapped[str] = mapped_column(String(255), nullable=True)
    utm_term: Mapped[str] = mapped_column(String(255), nullable=True)
    visit_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    # relationships
    gcft_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft.id"), nullable=False
    )
    snap_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft_snap.id"), nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GcftSnapTrafficsource({self.session_id} \
            on {self.visit_date}, referrer={self.referrer})"
        return repr_str
