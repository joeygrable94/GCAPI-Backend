from typing import TYPE_CHECKING

from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, ForeignKey

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .client import Client  # noqa: F401
    from .website import Website  # noqa: F401


class ClientWebsite(TableBase):
    __tablename__: str = "client_website"
    client_id: Column[str] = Column(GUID, ForeignKey("client.id"), nullable=False)
    website_id: Column[str] = Column(GUID, ForeignKey("website.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str: str = (
            f"ClientWebsite({self.id}, [C({self.client_id}), W({self.website_id})])"
        )
        return repr_str
