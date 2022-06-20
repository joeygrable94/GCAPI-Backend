from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, ForeignKey, String

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .client import Client  # noqa: F401


class SharpSpring(TableBase):
    __tablename__ = "sharpspring"
    hashed_api_key = Column(String(64), nullable=False)
    hashed_secret_key = Column(String(64), nullable=False)

    # relationships
    client_id = Column(CHAR(36), ForeignKey("client.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str = f"SharpSpring(Client[{self.client_id}] since {self.created_on})"
        return repr_str
