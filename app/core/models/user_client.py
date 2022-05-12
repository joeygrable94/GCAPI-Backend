from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, ForeignKey, String

from app.core.models.table_model import TableBase

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .client import Client  # noqa: F401


class UserClient(TableBase):
    """UserClient model relationships use an additional column
    `scope` to define the level of access the user has to the
    client data model.
    """
    __tablename__           = 'user_client'
    scope                   = Column(String(255), nullable=False, default='role:view')
    user_id                 = Column(CHAR(36), ForeignKey('user.id'), nullable=False)
    client_id               = Column(CHAR(36), ForeignKey('client.id'), nullable=False)

    def __repr__(self):
        repr_str = f'UserClient({self.id}, {self.scope}, [U({self.user_id}), C({self.client_id})])'
        return repr_str
