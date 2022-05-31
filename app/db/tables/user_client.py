from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, ForeignKey

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .client import Client  # noqa: F401
    from .user import User  # noqa: F401


class UserClient(TableBase):
    __tablename__ = "user_client"
    user_id = Column(CHAR(36), ForeignKey("user.id"), nullable=False)
    client_id = Column(CHAR(36), ForeignKey("client.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str = f"UserClient({self.id}, [U({self.user_id}), C({self.client_id})])"
        return repr_str
