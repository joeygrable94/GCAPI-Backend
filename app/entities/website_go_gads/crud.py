from app.core.crud import BaseRepository
from app.entities.website_go_gads.model import WebsiteGoAdsProperty
from app.entities.website_go_gads.schemas import (
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
