from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.schemas import WebsitePageSpeedInsightsCreate, WebsitePageSpeedInsightsRead, WebsitePageSpeedInsightsUpdate
from app.db.tables import WebsitePageSpeedInsights


class WebsitePageSpeedInsightsRepository(
    BaseRepository[
        WebsitePageSpeedInsightsCreate,
        WebsitePageSpeedInsightsRead,
        WebsitePageSpeedInsightsUpdate,
        WebsitePageSpeedInsights
    ]
):
    @property
    def _table(self) -> Type[WebsitePageSpeedInsights]:  # type: ignore
        return WebsitePageSpeedInsights
