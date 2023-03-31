from typing import Annotated, Any, List
from uuid import UUID

from fastapi import Depends, HTTPException, status, Query

from app.api.exceptions import InvalidID
from app.core.logger import logger
from app.core.utilities.uuids import parse_id
from app.schemas import PageSpeedInsightsDevice


class PageQueryParams:
    def __init__(self, page: int = 1):
        if page < 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Page number must be greater than 0",
            )
        self.page = page


class ClientQueryParams:
    def __init__(self, client_id: Any | None = None):
        q_client_id: UUID | None
        try:
            q_client_id = None if not client_id else parse_id(client_id)
        except InvalidID:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid client ID",
            )
        self.client_id: UUID | None = q_client_id


class WebsiteQueryParams:
    def __init__(self, website_id: Any | None = None):
        q_website_id: UUID | None
        try:
            q_website_id = None if not website_id else parse_id(website_id)
        except InvalidID:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid website ID",
            )
        self.website_id: UUID | None = q_website_id


class WebsiteMapQueryParams:
    def __init__(self, sitemap_id: Any | None = None):
        q_sitemap_id: UUID | None
        try:
            q_sitemap_id = None if not sitemap_id else parse_id(sitemap_id)
        except InvalidID:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid sitemap ID",
            )
        self.sitemap_id: UUID | None = q_sitemap_id


class WebsitePageQueryParams:
    def __init__(self, page_id: Any | None = None):
        q_page_id: UUID | None
        try:
            q_page_id = None if not page_id else parse_id(page_id)
        except InvalidID:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid page ID",
            )
        self.page_id: UUID | None = q_page_id


class DeviceStrategyQueryParams:
    def __init__(self, strategy: List[str] | None = None):
        q_devices: List[str] | None = None
        try:
            if strategy is not None:
                q_devices = []
                for stg in strategy:
                    device = PageSpeedInsightsDevice(device=stg)
                    q_devices.append(stg)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid strategy",
            )
        self.devices: List[str] | None = q_devices


class CommonQueryParams(PageQueryParams):
    def __init__(self, page: int = Query(1)):
        PageQueryParams.__init__(self, page)


GetQueryParams = Annotated[CommonQueryParams, Depends()]


class CommonClientQueryParams(PageQueryParams, ClientQueryParams):
    def __init__(
        self,
        page: int = 1,
        client_id: Any | None = Query(None),
    ):
        PageQueryParams.__init__(self, page)
        ClientQueryParams.__init__(self, client_id)


GetClientQueryParams = Annotated[CommonClientQueryParams, Depends()]


class CommonWebsiteQueryParams(PageQueryParams, WebsiteQueryParams):
    def __init__(
        self,
        page: int = 1,
        website_id: Any | None = Query(None),
    ):
        PageQueryParams.__init__(self, page)
        WebsiteQueryParams.__init__(self, website_id)


GetWebsiteQueryParams = Annotated[CommonClientQueryParams, Depends()]


class CommonClientWebsiteQueryParams(PageQueryParams, ClientQueryParams, WebsiteQueryParams):
    def __init__(
        self,
        page: int = 1,
        client_id: Any | None = Query(None),
        website_id: Any | None = Query(None),
    ):
        PageQueryParams.__init__(self, page)
        ClientQueryParams.__init__(self, client_id)
        WebsiteQueryParams.__init__(self, website_id)


GetClientWebsiteQueryParams = Annotated[CommonClientWebsiteQueryParams, Depends()]


class CommonWebsitePageQueryParams(PageQueryParams, WebsiteQueryParams, WebsiteMapQueryParams):
    def __init__(
        self,
        page: int = 1,
        website_id: Any | None = Query(None),
        sitemap_id: Any | None = Query(None),
    ):
        PageQueryParams.__init__(self, page)
        WebsiteQueryParams.__init__(self, website_id)
        WebsiteMapQueryParams.__init__(self, sitemap_id)


GetWebsitePageQueryParams = Annotated[CommonWebsitePageQueryParams, Depends()]


class CommonWebsiteMapQueryParams(PageQueryParams, WebsiteQueryParams):
    def __init__(
        self,
        page: int = 1,
        website_id: Any | None = Query(None),
    ):
        PageQueryParams.__init__(self, page)
        WebsiteQueryParams.__init__(self, website_id)


GetWebsiteMapQueryParams = Annotated[CommonWebsitePageQueryParams, Depends()]


class CommonWebsitePageSpeedInsightsQueryParams(
    PageQueryParams,
    WebsiteQueryParams,
    WebsitePageQueryParams,
    DeviceStrategyQueryParams
):
    def __init__(
        self,
        page: int = 1,
        website_id: Any | None = Query(None),
        page_id: Any | None = Query(None),
        strategy: List[str] | None = Query(None),
    ):
        PageQueryParams.__init__(self, page)
        WebsiteQueryParams.__init__(self, website_id)
        WebsitePageQueryParams.__init__(self, page_id)
        DeviceStrategyQueryParams.__init__(self, strategy)


GetWebsitePageSpeedInsightsQueryParams = Annotated[CommonWebsitePageSpeedInsightsQueryParams, Depends()]
