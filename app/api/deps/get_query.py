import datetime as dt
from typing import Annotated, List

from fastapi import Depends, HTTPException, Query, status
from pydantic import UUID4

from app.api.exceptions import GoSearchConsoleMetricTypeInvalid, InvalidID
from app.core.config import settings
from app.core.pagination import PageParamsFromQuery
from app.core.utilities.uuids import parse_id
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.schemas import GoSearchConsoleMetricType, PageSpeedInsightsDevice, PSIDevice

# utility query classes


class IsActiveQueryParams:
    def __init__(self, is_active: bool | None = None):
        self.is_active: bool | None = is_active


class DateStartQueryParams:
    def __init__(self, date_start: str | None = None):
        try:
            q_date_start = None if not date_start else dt.date.fromisoformat(date_start)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid date format",
            )
        self.date_start: dt.date | None = q_date_start


class DateEndQueryParams:
    def __init__(self, date_end: str | None = None):
        try:
            q_date_end = None if not date_end else dt.date.fromisoformat(date_end)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid date format",
            )
        self.date_end: dt.date | None = q_date_end


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
                    device = PageSpeedInsightsDevice(device=PSIDevice(stg))
                    q_devices.append(device.device.value)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid device strategy, must be 'mobile' or 'desktop'",
            )
        self.strategy: List[str] | None = q_devices


class Ga4QueryParams:
    def __init__(self, ga4_id: str | None = None):
        q_ga4_id: UUID4 | None
        try:
            q_ga4_id = None if not ga4_id else parse_id(ga4_id)
        except InvalidID:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid ga4 property ID",
            )
        self.ga4_id: UUID4 | None = q_ga4_id


class GoSearchConsoleMetricTypeQueryParams:
    def __init__(self, metric_types: str | None = None):
        s_metric_types: List[str] | None = None
        q_metric_types: List[GoSearchConsoleMetricType] | None = None
        try:
            s_metric_types = (
                None
                if metric_types is None or metric_types == ""
                else metric_types.split(",") if "," in metric_types else [metric_types]
            )
            q_metric_types = (
                None
                if s_metric_types is None
                else [GoSearchConsoleMetricType(metric) for metric in s_metric_types]
            )
        except ValueError:
            raise GoSearchConsoleMetricTypeInvalid()
        self.metric_types: list[GoSearchConsoleMetricType] | None = q_metric_types


class TrackingLinkUtmCampaignQueryParams:
    def __init__(self, utm_campaign: str | None = None):
        self.utm_campaign: str | None = utm_campaign


class TrackingLinkUtmMediumQueryParams:
    def __init__(self, utm_medium: str | None = None):
        self.utm_medium: str | None = utm_medium


class TrackingLinkUtmSourceQueryParams:
    def __init__(self, utm_source: str | None = None):
        self.utm_source: str | None = utm_source


class TrackingLinkUtmContentQueryParams:
    def __init__(self, utm_content: str | None = None):
        self.utm_content: str | None = utm_content


class TrackingLinkUtmTermQueryParams:
    def __init__(self, utm_term: str | None = None):
        self.utm_term: str | None = utm_term


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


class CommonWebsiteGa4QueryParams(
    PageParamsFromQuery, WebsiteIdQueryParams, Ga4QueryParams
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
        ga4_id: Annotated[str | None, Query()] = None,
    ):
        PageParamsFromQuery.__init__(self, page, size)
        WebsiteIdQueryParams.__init__(self, website_id)
        Ga4QueryParams.__init__(self, ga4_id)


GetWebsiteGa4QueryParams = Annotated[CommonWebsiteGa4QueryParams, Depends()]


class CommonWebsiteGoSearchConsoleQueryParams(
    PageParamsFromQuery,
    GoSearchConsoleMetricTypeQueryParams,
    DateStartQueryParams,
    DateEndQueryParams,
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
        metric_types: Annotated[str | None, Query()] = None,
        date_start: Annotated[str | None, Query()] = None,
        date_end: Annotated[str | None, Query()] = None,
    ):
        PageParamsFromQuery.__init__(self, page, size)
        GoSearchConsoleMetricTypeQueryParams.__init__(self, metric_types)
        DateStartQueryParams.__init__(self, date_start)
        DateEndQueryParams.__init__(self, date_end)


GetWebsiteGoSearchConsoleQueryParams = Annotated[
    CommonWebsiteGoSearchConsoleQueryParams, Depends()
]


class CommonClientTrackingLinkQueryParams(
    PageParamsFromQuery,
    ClientIdQueryParams,
    TrackingLinkUtmCampaignQueryParams,
    TrackingLinkUtmMediumQueryParams,
    TrackingLinkUtmSourceQueryParams,
    TrackingLinkUtmContentQueryParams,
    TrackingLinkUtmTermQueryParams,
    IsActiveQueryParams,
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
        utm_campaign: Annotated[
            str | None, Query(max_length=DB_STR_TINYTEXT_MAXLEN_INPUT)
        ] = None,
        utm_medium: Annotated[
            str | None, Query(max_length=DB_STR_TINYTEXT_MAXLEN_INPUT)
        ] = None,
        utm_source: Annotated[
            str | None, Query(max_length=DB_STR_TINYTEXT_MAXLEN_INPUT)
        ] = None,
        utm_content: Annotated[
            str | None, Query(max_length=DB_STR_TINYTEXT_MAXLEN_INPUT)
        ] = None,
        utm_term: Annotated[
            str | None, Query(max_length=DB_STR_TINYTEXT_MAXLEN_INPUT)
        ] = None,
        is_active: Annotated[bool | None, Query()] = None,
    ):
        PageParamsFromQuery.__init__(self, page, size)
        ClientIdQueryParams.__init__(self, client_id)
        TrackingLinkUtmCampaignQueryParams.__init__(self, utm_campaign)
        TrackingLinkUtmMediumQueryParams.__init__(self, utm_medium)
        TrackingLinkUtmSourceQueryParams.__init__(self, utm_source)
        TrackingLinkUtmContentQueryParams.__init__(self, utm_content)
        TrackingLinkUtmTermQueryParams.__init__(self, utm_term)
        IsActiveQueryParams.__init__(self, is_active)


GetClientTrackingLinkQueryParams = Annotated[
    CommonClientTrackingLinkQueryParams, Depends()
]
