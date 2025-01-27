from app.crud.base import BaseRepository
from app.models import WebsiteGoAnalytics4Property
from app.schemas import (
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
