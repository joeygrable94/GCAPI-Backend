from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, ForeignKey, String, Text

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Item(TableBase):
    __tablename__ = "item"
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)

    # relationships
    user_id = Column(CHAR(36), ForeignKey("user.id"), nullable=True)

    def __repr__(self) -> str:
        repr_str = f"Item({self.title} by {self.user_id} on {self.updated_on})"
        return repr_str
