from pydantic import UUID4

from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class WebsiteGoAdsPropertyBase(BaseSchema):
    website_id: UUID4
    go_ads_id: UUID4


class WebsiteGoAdsPropertyCreate(WebsiteGoAdsPropertyBase):
    pass


class WebsiteGoAdsPropertyUpdate(BaseSchema):
    website_id: UUID4 | None = None
    go_ads_id: UUID4 | None = None


class WebsiteGoAdsPropertyRead(WebsiteGoAdsPropertyBase, BaseSchemaRead):
    id: UUID4
