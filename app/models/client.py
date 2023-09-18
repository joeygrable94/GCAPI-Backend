from datetime import datetime
from typing import TYPE_CHECKING, Any, List

from pydantic import UUID4
from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .bdx_feed import BdxFeed  # noqa: F401
    from .client_bucket import ClientBucket  # noqa: F401
    from .client_report import ClientReport  # noqa: F401
    from .go_a4 import GoAnalytics4Property  # noqa: F401
    from .go_cloud import GoCloudProperty  # noqa: F401
    from .go_ua import GoUniversalAnalyticsProperty  # noqa: F401
    from .sharpspring import Sharpspring  # noqa: F401
    from .user import User  # noqa: F401
    from .website import Website  # noqa: F401


class Client(Base):
    __tablename__: str = "client"
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
    title: Mapped[str] = mapped_column(
        String(96), nullable=False, unique=True, primary_key=True
    )
    description: Mapped[str] = mapped_column(Text(5000), nullable=True)

    # relationships
    users: Mapped[List["User"]] = relationship(
        "User", secondary="user_client", back_populates="clients"
    )
    websites: Mapped[List["Website"]] = relationship(
        "Website", secondary="client_website", back_populates="clients"
    )
    client_reports: Mapped[List["ClientReport"]] = relationship(
        "ClientReport", backref=backref("client", lazy="noload")
    )
    gcloud_accounts: Mapped[List["GoCloudProperty"]] = relationship(
        "GoCloudProperty", backref=backref("client", lazy="noload")
    )
    ga4_accounts: Mapped[List["GoAnalytics4Property"]] = relationship(
        "GoAnalytics4Property", backref=backref("client", lazy="noload")
    )
    gua_accounts: Mapped[List["GoUniversalAnalyticsProperty"]] = relationship(
        "GoUniversalAnalyticsProperty", backref=backref("client", lazy="noload")
    )
    sharpspring_accounts: Mapped[List["Sharpspring"]] = relationship(
        "Sharpspring", backref=backref("client", lazy="noload")
    )
    buckets: Mapped[List["ClientBucket"]] = relationship(
        "ClientBucket", backref=backref("client", lazy="noload")
    )
    bdx_feeds: Mapped[List["BdxFeed"]] = relationship(
        "BdxFeed", backref=backref("client", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Client({self.title}, since {self.created_on})"
        return repr_str
