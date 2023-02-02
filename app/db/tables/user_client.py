from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .user import User  # noqa: F401


class UserClient(TableBase):
    __tablename__: str = "user_client"

    # relationships
    user_id: Column[UUID] = Column(
        GUID, ForeignKey("user.id"), primary_key=True, nullable=False
    )
    client_id: Column[UUID] = Column(
        GUID, ForeignKey("client.id"), primary_key=True, nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"UserClient({self.id}, [U({self.user_id}), C({self.client_id})])"
        )
        return repr_str
