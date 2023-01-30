from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401


class SharpSpring(TableBase):
    __tablename__: str = "sharpspring"
    hashed_api_key: Column[str] = Column(String(64), nullable=False)
    hashed_secret_key: Column[str] = Column(String(64), nullable=False)

    # relationships
    client_id: Column[UUID] = Column(GUID, ForeignKey("client.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"SharpSpring(Client[{self.client_id}] since {self.created_on})"
        return repr_str
