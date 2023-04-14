from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import UUID4
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .geocoord import GeoCoord  # noqa: F401


class ImageUpload(Base):
    __tablename__: str = "imageupload"
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
    file_name: Mapped[str] = mapped_column(
        String(120), nullable=False, default="default.jpg"
    )
    file_path: Mapped[str] = mapped_column(
        String(255), nullable=False, default="uploads/tmp"
    )
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    caption: Mapped[str] = mapped_column(String(255), nullable=True)
    is_geotagged: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

    # relationships
    user_id: Mapped[str] = mapped_column(String(128), nullable=True)
    geocoord_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("geocoord.id"), nullable=True
    )
    geotag: Mapped["GeoCoord"] = relationship(
        "GeoCoord", backref=backref("imageupload", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"ImageUpload({self.title}: \
            created {self.created_on}, updated {self.updated_on})"
        return repr_str
