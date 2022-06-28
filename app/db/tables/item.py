from typing import TYPE_CHECKING, Optional

from sqlalchemy import CHAR, Column, ForeignKey, String, Text

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Item(TableBase):
    __tablename__: str = "item"
    title: Column[str] = Column(String(255), nullable=False)
    content: Column[Optional[str]] = Column(Text, nullable=True)

    # relationships
    user_id: Column[Optional[str]] = Column(
        CHAR(36), ForeignKey("user.id"), nullable=True
    )

    def __repr__(self) -> str:
        repr_str: str = f"Item({self.title} by {self.user_id} on {self.updated_on})"
        return repr_str
