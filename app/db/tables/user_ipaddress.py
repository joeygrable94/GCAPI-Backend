from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Mapped

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .ipaddress import IpAddress  # noqa: F401
    from .user import User  # noqa: F401


class UserIpAddress(TableBase):
    __tablename__: str = "user_ipaddress"
    user_id: Mapped[UUID] = Column(GUID, ForeignKey("user.id"), nullable=False)
    ipaddress_id: Mapped[UUID] = Column(
        GUID, ForeignKey("ipaddress.id"), nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"UserIpAddress({self.id}, [U({self.user_id}), IP({self.ipaddress_id})])"
        )
        return repr_str
