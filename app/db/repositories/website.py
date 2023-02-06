from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.schemas import WebsiteCreate, WebsiteRead, WebsiteUpdate
from app.db.tables import Website


class WebsiteRepository(
    BaseRepository[WebsiteCreate, WebsiteRead, WebsiteUpdate, Website]
):
    @property
    def _table(self) -> Type[Website]:  # type: ignore
        return Website
