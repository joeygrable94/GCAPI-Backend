from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey, String, Text

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Item(TableBase):
    __tablename__ = "item"
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(GUID, ForeignKey("user.id"), nullable=True)

    def __repr__(self):
        repr_str = f"Item({self.title} by {self.user_id} on {self.updated_on})"
        return repr_str
