from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import Timestamp  # type: ignore
from sqlalchemy_utils import UUIDType

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .tracking_link import TrackingLink  # noqa: F401


class ClientTrackingLink(Base, Timestamp):
    __tablename__: str = "client_tracking_link"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("client.id"),
        primary_key=True,
        nullable=False,
    )
    tracking_link_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("tracking_link.id"),
        primary_key=True,
        nullable=False,
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"ClientTrackingLink({self.id}, [C({self.client_id}), L({self.tracking_link_id})])"  # noqa: E501
        )
        return repr_str
