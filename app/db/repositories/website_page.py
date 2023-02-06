from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.schemas import WebsitePageCreate, WebsitePageRead, WebsitePageUpdate
from app.db.tables import WebsitePage


class WebsitePageRepository(
    BaseRepository[WebsitePageCreate, WebsitePageRead, WebsitePageUpdate, WebsitePage]
):
    @property
    def _table(self) -> Type[WebsitePage]:  # type: ignore
        return WebsitePage
