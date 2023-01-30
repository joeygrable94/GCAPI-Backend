from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:  # pragma: no cover
    from .client_website import ClientWebsite  # noqa: F401
    from .go_a4 import GoogleAnalytics4Property  # noqa: F401
    from .go_cloud import GoogleCloudProperty  # noqa: F401
    from .go_ua import GoogleUniversalAnalyticsProperty  # noqa: F401
    from .sharpspring import SharpSpring  # noqa: F401
    from .user import User  # noqa: F401
    from .user_client import UserClient  # noqa: F401
    from .website import Website  # noqa: F401


class Client(TableBase):
    __tablename__: str = "client"
    title: Column[str] = Column(String(96), nullable=False)
    content: Column[Optional[str]] = Column(String(255), nullable=True)

    # relationships
    users: Column[Optional[List["User"]]] = relationship(  # type: ignore
        "User", secondary="user_client", back_populates="clients"
    )
    websites: Column[Optional[List["Website"]]] = relationship(  # type: ignore
        "Website", secondary="client_website", back_populates="clients"
    )
    gcloud_accounts: Column[
        Optional[List["GoogleCloudProperty"]]
    ] = relationship(  # type: ignore
        "GoogleCloudProperty", backref=backref("client", lazy="noload")
    )
    ga4_accounts: Column[
        Optional[List["GoogleAnalytics4Property"]]
    ] = relationship(  # type: ignore
        "GoogleAnalytics4Property", backref=backref("client", lazy="noload")
    )
    gua_accounts: Column[
        Optional[List["GoogleUniversalAnalyticsProperty"]]
    ] = relationship(  # type: ignore
        "GoogleUniversalAnalyticsProperty", backref=backref("client", lazy="noload")
    )
    sharpspring_accounts: Column[
        Optional[List["SharpSpring"]]
    ] = relationship(  # type: ignore
        "SharpSpring", backref=backref("client", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Client({self.title}, since {self.created_on})"
        return repr_str
