from app.core.crud import BaseRepository
from app.entities.website_go_ga4.model import WebsiteGoAnalytics4Property
from app.entities.website_go_ga4.schemas import (
    WebsiteGoAnalytics4PropertyCreate,
    WebsiteGoAnalytics4PropertyRead,
    WebsiteGoAnalytics4PropertyUpdate,
)


class WebsiteGoAnalytics4PropertyRepository(
    BaseRepository[
        WebsiteGoAnalytics4PropertyCreate,
        WebsiteGoAnalytics4PropertyRead,
        WebsiteGoAnalytics4PropertyUpdate,
        WebsiteGoAnalytics4Property,
    ]
):
    @property
    def _table(self) -> WebsiteGoAnalytics4Property:
        return WebsiteGoAnalytics4Property
