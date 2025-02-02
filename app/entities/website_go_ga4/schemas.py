from pydantic import UUID4

from app.core.schema import BaseSchema, BaseSchemaRead


class WebsiteGoAnalytics4PropertyBase(BaseSchema):
    website_id: UUID4
    go_a4_id: UUID4


class WebsiteGoAnalytics4PropertyCreate(WebsiteGoAnalytics4PropertyBase):
    pass


class WebsiteGoAnalytics4PropertyUpdate(BaseSchema):
    website_id: UUID4 | None = None
    go_a4_id: UUID4 | None = None


class WebsiteGoAnalytics4PropertyRead(WebsiteGoAnalytics4PropertyBase, BaseSchemaRead):
    id: UUID4
