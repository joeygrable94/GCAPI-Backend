from app.crud.base import BaseRepository
from app.models import WebsiteGoAdsProperty
from app.schemas import (
    WebsiteGoAdsPropertyCreate,
    WebsiteGoAdsPropertyRead,
    WebsiteGoAdsPropertyUpdate,
)


class WebsiteGoAdsPropertyRepository(
    BaseRepository[
        WebsiteGoAdsPropertyCreate,
        WebsiteGoAdsPropertyRead,
        WebsiteGoAdsPropertyUpdate,
        WebsiteGoAdsProperty,
    ]
):
    @property
    def _table(self) -> WebsiteGoAdsProperty:
        return WebsiteGoAdsProperty
