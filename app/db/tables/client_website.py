from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .website import Website  # noqa: F401


class ClientWebsite(TableBase):
    __tablename__: str = "client_website"
    client_id: Column[UUID] = Column(GUID, ForeignKey("client.id"), nullable=False)
    website_id: Column[UUID] = Column(GUID, ForeignKey("website.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"ClientWebsite({self.id}, [C({self.client_id}), W({self.website_id})])"
        )
        return repr_str
