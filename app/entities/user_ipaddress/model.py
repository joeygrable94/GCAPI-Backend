from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import Timestamp, UUIDType

from app.db.base_class import Base
from app.utilities import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    pass


class UserIpaddress(Base, Timestamp):
    __tablename__: str = "user_ipaddress"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid,
    )
    user_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("user.id"),
        primary_key=True,
        nullable=False,
    )
    ipaddress_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("ipaddress.id"),
        primary_key=True,
        nullable=False,
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"UserIpaddress({self.id}, [U({self.user_id}), I({self.ipaddress_id})])"
        )
        return repr_str
