from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.schemas import WebsiteCreate, WebsiteRead, WebsiteUpdate
from app.db.tables import Website


class WebsitesRepository(
    BaseRepository[WebsiteCreate, WebsiteRead, WebsiteUpdate, Website]
):
    @property
    def _schema_read(self) -> Type[WebsiteRead]:  # type: ignore
        return WebsiteRead

    @property
    def _table(self) -> Type[Website]:  # type: ignore
        return Website
