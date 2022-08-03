from typing import TYPE_CHECKING

from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, ForeignKey, String, Text

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Note(TableBase):
    __tablename__: str = "note"
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)

    # relationships
    user_id = Column(GUID, ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str: str = f"Item({self.title} by {self.user_id} on {self.updated_on})"
        return repr_str
