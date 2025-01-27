from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import Timestamp, UUIDType

from app.core.utilities import get_uuid
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .website import Website  # noqa: F401


class ClientWebsite(Base, Timestamp):
    __tablename__: str = "client_website"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid,
    )
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("client.id"),
        primary_key=True,
        nullable=False,
    )
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("website.id"),
        primary_key=True,
        nullable=False,
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"ClientWebsite({self.id}, [C({self.client_id}), W({self.website_id})])"
        )
        return repr_str
