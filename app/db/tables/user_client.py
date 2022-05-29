from typing import TYPE_CHECKING
from fastapi_users_db_sqlalchemy import GUID

from sqlalchemy import CHAR, Column, ForeignKey

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .client import Client  # noqa: F401


class UserClient(TableBase):
    __tablename__           = 'user_client'
    user_id                 = Column(GUID, ForeignKey('user.id'), nullable=False)
    client_id               = Column(GUID, ForeignKey('client.id'), nullable=False)

    def __repr__(self):
        repr_str = f'UserClient({self.id}, [U({self.user_id}), C({self.client_id})])'
        return repr_str
