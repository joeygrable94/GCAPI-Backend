from datetime import datetime
from typing import TYPE_CHECKING, Any, List

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .go_a4_stream import GoogleAnalytics4Stream  # noqa: F401
    from .website import Website  # noqa: F401


class GoogleAnalytics4Property(Base):
    __tablename__: str = "go_a4"
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
    measurement_id: Mapped[str] = mapped_column(
        String(16), nullable=False, unique=True, primary_key=True
    )
    property_id: Mapped[str] = mapped_column(String(16), nullable=False, index=True)

    # relationships
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client.id"), nullable=False
    )
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website.id"), nullable=False
    )
    ga4_streams: Mapped[List["GoogleAnalytics4Stream"]] = relationship(
        "GoogleAnalytics4Stream",
        backref=backref("go_a4", lazy="subquery"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GoogleAnalytics4Property(\
            MeasurementID[{self.measurement_id}] for \
            Client[{self.client_id}] \
            Website[{self.website_id}])"
        return repr_str
