from typing import TYPE_CHECKING, Any, List, Optional

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import Mapped, backref, relationship

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
    title: Mapped[str] = Column(String(96), nullable=False)
    content: Mapped[str] = Column(Text, nullable=True)

    # relationships
    users: Mapped[Optional[List[Any]]] = relationship(
        "User", secondary="user_client", back_populates="clients"
    )
    websites: Mapped[Optional[List[Any]]] = relationship(
        "Website", secondary="client_website", back_populates="clients"
    )
    gcloud_accounts: Mapped[Optional[List[Any]]] = relationship(
        "GoogleCloudProperty", backref=backref("client", lazy="noload")
    )
    ga4_accounts: Mapped[Optional[List[Any]]] = relationship(
        "GoogleAnalytics4Property", backref=backref("client", lazy="noload")
    )
    gua_accounts: Mapped[Optional[List[Any]]] = relationship(
        "GoogleUniversalAnalyticsProperty", backref=backref("client", lazy="noload")
    )
    sharpspring_accounts: Mapped[Optional[List[Any]]] = relationship(
        "SharpSpring", backref=backref("client", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Client({self.title}, since {self.created_on})"
        return repr_str
