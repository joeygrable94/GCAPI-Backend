from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String, Text

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .user import User  # noqa: F401


class Note(TableBase):
    __tablename__: str = "note"
    title: Column[str] = Column(String(255), nullable=False)
    content: Column[str] = Column(Text, nullable=False)

    # relationships
    user_id: Column[UUID] = Column(GUID, ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Item({self.title} by {self.user_id} on {self.updated_on})"
        return repr_str
