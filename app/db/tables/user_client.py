from typing import TYPE_CHECKING

from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, ForeignKey

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .client import Client  # noqa: F401
    from .user import User  # noqa: F401


class UserClient(TableBase):
    __tablename__: str = "user_client"

    # relationships
    user_id = Column(GUID, ForeignKey("user.id"), nullable=False)
    client_id = Column(GUID, ForeignKey("client.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str: str = (
            f"UserClient({self.id}, [U({self.user_id}), C({self.client_id})])"
        )
        return repr_str
