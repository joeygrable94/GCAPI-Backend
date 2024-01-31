from typing import Annotated, List

from fastapi import Depends, HTTPException, Query, status
from pydantic import UUID4

from app.api.exceptions import InvalidID
from app.core.config import settings
from app.core.pagination import PageParamsFromQuery
from app.core.utilities.uuids import parse_id
from app.schemas import PageSpeedInsightsDevice

# utility query classes


class UserIdQueryParams:
    def __init__(self, user_id: str | None = None):
        q_user_id: UUID4 | None
        try:
            q_user_id = None if not user_id else parse_id(user_id)
        except InvalidID:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid user ID",
            )
        self.user_id: UUID4 | None = q_user_id


class ClientIdQueryParams:
    def __init__(self, client_id: str | None = None):
        q_client_id: UUID4 | None
        try:
            q_client_id = None if not client_id else parse_id(client_id)
        except InvalidID:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid client ID",
            )
        self.client_id: UUID4 | None = q_client_id


class WebsiteIdQueryParams:
    def __init__(self, website_id: str | None = None):
        q_website_id: UUID4 | None
        try:
            q_website_id = None if not website_id else parse_id(website_id)
        except InvalidID:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid website ID",
            )
        self.website_id: UUID4 | None = q_website_id


class WebsiteMapIdQueryParams:
    def __init__(self, sitemap_id: str | None = None):
        q_sitemap_id: UUID4 | None
        try:
            q_sitemap_id = None if not sitemap_id else parse_id(sitemap_id)
        except InvalidID:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid sitemap ID",
            )
        self.sitemap_id: UUID4 | None = q_sitemap_id


class WebsitePageIdQueryParams:
    def __init__(self, page_id: str | None = None):
        q_page_id: UUID4 | None
        try:
            q_page_id = None if not page_id else parse_id(page_id)
        except InvalidID:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid page ID",
            )
        self.page_id: UUID4 | None = q_page_id


class DeviceStrategyQueryParams:
    def __init__(self, strategy: List[str] | None = None):
        q_devices: List[str] | None = None
        try:
            if strategy is not None:
                q_devices = []
                for stg in strategy:
                    device = PageSpeedInsightsDevice(device=stg)
                    q_devices.append(device.device)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid device strategy, must be 'mobile' or 'desktop'",
            )
        self.strategy: List[str] | None = q_devices


# compound query classes


class PublicQueryParams:
    def __init__(self, message: Annotated[str | None, Query(max_length=50)] = None):
        self.message = message


GetPublicQueryParams = Annotated[PublicQueryParams, Depends()]


class CommonUserQueryParams(PageParamsFromQuery, UserIdQueryParams):
    def __init__(
        self,
        page: Annotated[int | None, Query(ge=1)] = 1,
        size: Annotated[
            int | None,
            Query(
                ge=1,
                le=settings.api.query_limit_rows_max,
            ),
        ] = settings.api.query_limit_rows_default,
        user_id: Annotated[str | None, Query()] = None,
    ):
        PageParamsFromQuery.__init__(self, page, size)
        UserIdQueryParams.__init__(self, user_id)


GetUserQueryParams = Annotated[CommonUserQueryParams, Depends()]


class CommonClientQueryParams(PageParamsFromQuery, ClientIdQueryParams):
    def __init__(
        self,
        page: Annotated[int | None, Query(ge=1)] = 1,
        size: Annotated[
            int | None,
            Query(
                ge=1,
                le=settings.api.query_limit_rows_max,
            ),
        ] = settings.api.query_limit_rows_default,
        client_id: Annotated[str | None, Query()] = None,
    ):
        PageParamsFromQuery.__init__(self, page, size)
        ClientIdQueryParams.__init__(self, client_id)


GetClientQueryParams = Annotated[CommonClientQueryParams, Depends()]


class CommonUserClientQueryParams(
    PageParamsFromQuery, UserIdQueryParams, ClientIdQueryParams
):
    def __init__(
        self,
        page: Annotated[int | None, Query(ge=1)] = 1,
        size: Annotated[
            int | None,
            Query(
                ge=1,
                le=settings.api.query_limit_rows_max,
            ),
        ] = settings.api.query_limit_rows_default,
        user_id: Annotated[str | None, Query()] = None,
        client_id: Annotated[str | None, Query()] = None,
    ):
        PageParamsFromQuery.__init__(self, page, size)
        UserIdQueryParams.__init__(self, user_id)
        ClientIdQueryParams.__init__(self, client_id)


GetUserClientQueryParams = Annotated[CommonUserClientQueryParams, Depends()]


class CommonWebsiteQueryParams(PageParamsFromQuery, WebsiteIdQueryParams):
    def __init__(
        self,
        page: Annotated[int | None, Query(ge=1)] = 1,
        size: Annotated[
            int | None,
            Query(
                ge=1,
                le=settings.api.query_limit_rows_max,
            ),
        ] = settings.api.query_limit_rows_default,
        website_id: Annotated[str | None, Query()] = None,
    ):
        PageParamsFromQuery.__init__(self, page, size)
        WebsiteIdQueryParams.__init__(self, website_id)


GetWebsiteQueryParams = Annotated[CommonClientQueryParams, Depends()]


class CommonClientWebsiteQueryParams(
    PageParamsFromQuery, ClientIdQueryParams, WebsiteIdQueryParams
):
    def __init__(
        self,
        page: Annotated[int | None, Query(ge=1)] = 1,
        size: Annotated[
            int | None,
            Query(
                ge=1,
                le=settings.api.query_limit_rows_max,
            ),
        ] = settings.api.query_limit_rows_default,
        client_id: Annotated[str | None, Query()] = None,
        website_id: Annotated[str | None, Query()] = None,
    ):
        PageParamsFromQuery.__init__(self, page, size)
        ClientIdQueryParams.__init__(self, client_id)
        WebsiteIdQueryParams.__init__(self, website_id)


GetClientWebsiteQueryParams = Annotated[CommonClientWebsiteQueryParams, Depends()]


class CommonWebsitePageQueryParams(
    PageParamsFromQuery, WebsiteIdQueryParams, WebsiteMapIdQueryParams
):
    def __init__(
        self,
        page: Annotated[int | None, Query(ge=1)] = 1,
        size: Annotated[
            int | None,
            Query(
                ge=1,
                le=settings.api.query_limit_rows_max,
            ),
        ] = settings.api.query_limit_rows_default,
        website_id: Annotated[str | None, Query()] = None,
        sitemap_id: Annotated[str | None, Query()] = None,
    ):
        PageParamsFromQuery.__init__(self, page, size)
        WebsiteIdQueryParams.__init__(self, website_id)
        WebsiteMapIdQueryParams.__init__(self, sitemap_id)


GetWebsitePageQueryParams = Annotated[CommonWebsitePageQueryParams, Depends()]


class CommonWebsiteMapQueryParams(PageParamsFromQuery, WebsiteIdQueryParams):
    def __init__(
        self,
        page: Annotated[int | None, Query(ge=1)] = 1,
        size: Annotated[
            int | None,
            Query(
                ge=1,
                le=settings.api.query_limit_rows_max,
            ),
        ] = settings.api.query_limit_rows_default,
        website_id: Annotated[str | None, Query()] = None,
    ):
        PageParamsFromQuery.__init__(self, page, size)
        WebsiteIdQueryParams.__init__(self, website_id)


GetWebsiteMapQueryParams = Annotated[CommonWebsitePageQueryParams, Depends()]


class CommonWebsitePageSpeedInsightsQueryParams(
    PageParamsFromQuery,
    WebsiteIdQueryParams,
    WebsitePageIdQueryParams,
    DeviceStrategyQueryParams,
):
    def __init__(
        self,
        page: Annotated[int | None, Query(ge=1)] = 1,
        size: Annotated[
            int | None,
            Query(
                ge=1,
                le=settings.api.query_limit_rows_max,
            ),
        ] = settings.api.query_limit_rows_default,
        website_id: Annotated[str | None, Query()] = None,
        page_id: Annotated[str | None, Query()] = None,
        strategy: Annotated[List[str] | None, Query()] = None,
    ):
        PageParamsFromQuery.__init__(self, page, size)
        WebsiteIdQueryParams.__init__(self, website_id)
        WebsitePageIdQueryParams.__init__(self, page_id)
        DeviceStrategyQueryParams.__init__(self, strategy)


GetWebsitePageSpeedInsightsQueryParams = Annotated[
    CommonWebsitePageSpeedInsightsQueryParams, Depends()
]


class CommonWebsiteKeywordCorpusQueryParams(
    PageParamsFromQuery,
    WebsiteIdQueryParams,
    WebsitePageIdQueryParams,
):
    def __init__(
        self,
        page: Annotated[int | None, Query(ge=1)] = 1,
        size: Annotated[
            int | None,
            Query(
                ge=1,
                le=settings.api.query_limit_rows_max,
            ),
        ] = settings.api.query_limit_rows_default,
        website_id: Annotated[str | None, Query()] = None,
        page_id: Annotated[str | None, Query()] = None,
    ):
        PageParamsFromQuery.__init__(self, page, size)
        WebsiteIdQueryParams.__init__(self, website_id)
        WebsitePageIdQueryParams.__init__(self, page_id)


GetWebsiteKeywordCorpusQueryParams = Annotated[
    CommonWebsiteKeywordCorpusQueryParams, Depends()
]
