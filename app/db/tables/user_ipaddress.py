from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, ForeignKey

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .ipaddress import IpAddress  # noqa: F401
    from .user import User  # noqa: F401


class UserIpAddress(TableBase):
    __tablename__ = "user_ipaddress"
    user_id = Column(CHAR(36), ForeignKey("user.id"), nullable=False)
    ipaddress_id = Column(CHAR(36), ForeignKey("ipaddress.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str = (
            f"UserIpAddress({self.id}, [U({self.user_id}), IP({self.ipaddress_id})])"
        )
        return repr_str
