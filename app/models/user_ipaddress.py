from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .ipaddress import Ipaddress  # noqa: F401
    from .user import User  # noqa: F401


class UserIpaddress(Base):
    __tablename__: str = "user_ipaddress"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        primary_key=True,
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
    user_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("user.id"),
        nullable=False,
    )
    ipaddress_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("ipaddress.id"),
        nullable=False,
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"UserIpaddress({self.id}, [U({self.user_id}), I({self.ipaddress_id})])"
        )
        return repr_str
