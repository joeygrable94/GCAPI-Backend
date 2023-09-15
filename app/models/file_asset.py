from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import UUID4
from sqlalchemy import BLOB, INT, Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .geocoord import GeoCoord  # noqa: F401


class FileAsset(Base):
    __tablename__: str = "file_asset"
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
    name: Mapped[str] = mapped_column(
        String(96),
        nullable=False,
        unique=True,
        primary_key=True,
        default="default",
    )
    extension: Mapped[str] = mapped_column(String(255), nullable=False, default="jpg")
    size_kb: Mapped[int] = mapped_column(INT, nullable=False, default=0)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    tags: Mapped[str] = mapped_column(BLOB, nullable=True)
    is_private: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # relationships
    user_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("user.id"), nullable=False
    )
    bucket_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client_bucket.id"), nullable=False
    )
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client.id"), nullable=False
    )
    geocoord_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("geocoord.id"), nullable=True
    )
    bdx_feed_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("bdx_feed.id"), nullable=True
    )
    geotag: Mapped["GeoCoord"] = relationship(
        "GeoCoord", backref=backref("file_asset", lazy="subquery")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"FileAsset({self.title} | {self.name}.{self.extension} \
            [{self.size_kb} kb]: created {self.created_on}, updated {self.updated_on})"
        return repr_str
