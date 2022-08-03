from typing import TYPE_CHECKING

from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, ForeignKey, String

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .client import Client  # noqa: F401


class SharpSpring(TableBase):
    __tablename__: str = "sharpspring"
    hashed_api_key = Column(String(64), nullable=False)
    hashed_secret_key = Column(String(64), nullable=False)

    # relationships
    client_id = Column(GUID, ForeignKey("client.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str: str = f"SharpSpring(Client[{self.client_id}] since {self.created_on})"
        return repr_str
