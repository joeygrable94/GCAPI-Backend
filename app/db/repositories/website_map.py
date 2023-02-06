from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.schemas import WebsiteMapCreate, WebsiteMapRead, WebsiteMapUpdate
from app.db.tables import WebsiteMap


class WebsiteMapRepository(
    BaseRepository[WebsiteMapCreate, WebsiteMapRead, WebsiteMapUpdate, WebsiteMap]
):
    @property
    def _table(self) -> Type[WebsiteMap]:  # type: ignore
        return WebsiteMap
