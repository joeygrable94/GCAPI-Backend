import datetime as dt
import uuid

import pytest
from fastapi import HTTPException, status

from app.api.deps.get_query import (
    ClientIdQueryParams,
    CommonClientQueryParams,
    CommonClientWebsiteQueryParams,
    CommonUserClientQueryParams,
    CommonUserQueryParams,
    CommonWebsiteGa4QueryParams,
    CommonWebsiteGoSearchConsoleQueryParams,
    CommonWebsiteKeywordCorpusQueryParams,
    CommonWebsiteMapQueryParams,
    CommonWebsitePageQueryParams,
    CommonWebsitePageSpeedInsightsQueryParams,
    CommonWebsiteQueryParams,
    DateEndQueryParams,
    DateStartQueryParams,
    DeviceStrategyQueryParams,
    Ga4QueryParams,
    GoSearchConsoleMetricTypeQueryParams,
    PublicQueryParams,
    UserIdQueryParams,
    WebsiteIdQueryParams,
    WebsiteMapIdQueryParams,
    WebsitePageIdQueryParams,
)
from app.api.exceptions.exceptions import GoSearchConsoleMetricTypeInvalid
from app.core.config import settings
from app.core.utilities.uuids import get_uuid_str
from app.schemas import GoSearchConsoleMetricType


def test_user_id_query_params_valid_id() -> None:
    user_id = get_uuid_str()
    query_params = UserIdQueryParams(user_id=user_id)
    assert query_params.user_id == uuid.UUID(user_id)


def test_user_id_query_params_invalid_id() -> None:
    user_id = "invalid-id"
    try:
        UserIdQueryParams(user_id=user_id)
    except HTTPException as e:
        assert e.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert e.detail == "Invalid user ID"


def test_client_id_query_params_valid_id() -> None:
    client_id = get_uuid_str()
    query_params = ClientIdQueryParams(client_id=client_id)
    assert query_params.client_id == uuid.UUID(client_id)


def test_client_id_query_params_invalid_id() -> None:
    client_id = "invalid-id"
    try:
        ClientIdQueryParams(client_id=client_id)
    except HTTPException as e:
        assert e.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert e.detail == "Invalid client ID"


def test_client_id_query_params_none() -> None:
    query_params = ClientIdQueryParams()
    assert query_params.client_id is None


def test_website_id_query_params_valid_id() -> None:
    website_id = get_uuid_str()
    query_params = WebsiteIdQueryParams(website_id=website_id)
    assert query_params.website_id == uuid.UUID(website_id)


def test_website_id_query_params_invalid_id() -> None:
    website_id = "invalid-id"
    try:
        WebsiteIdQueryParams(website_id=website_id)
    except HTTPException as e:
        assert e.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert e.detail == "Invalid website ID"


def test_website_id_query_params_none() -> None:
    query_params = WebsiteIdQueryParams()
    assert query_params.website_id is None


def test_website_map_id_query_params_valid_id() -> None:
    sitemap_id = get_uuid_str()
    query_params = WebsiteMapIdQueryParams(sitemap_id=sitemap_id)
    assert query_params.sitemap_id == uuid.UUID(sitemap_id)


def test_website_map_id_query_params_invalid_id() -> None:
    sitemap_id = "invalid-id"
    try:
        WebsiteMapIdQueryParams(sitemap_id=sitemap_id)
    except HTTPException as e:
        assert e.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert e.detail == "Invalid sitemap ID"


def test_website_map_id_query_params_none() -> None:
    query_params = WebsiteMapIdQueryParams()
    assert query_params.sitemap_id is None


def test_website_page_id_query_params_valid_id() -> None:
    page_id = get_uuid_str()
    query_params = WebsitePageIdQueryParams(page_id=page_id)
    assert query_params.page_id == uuid.UUID(page_id)


def test_website_page_id_query_params_invalid_id() -> None:
    page_id = "invalid-id"
    try:
        WebsitePageIdQueryParams(page_id=page_id)
    except HTTPException as e:
        assert e.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert e.detail == "Invalid page ID"


def test_website_page_id_query_params_none() -> None:
    query_params = WebsitePageIdQueryParams()
    assert query_params.page_id is None


def test_device_strategy_query_params_valid_strategy() -> None:
    strategy = ["desktop", "mobile"]
    query_params = DeviceStrategyQueryParams(strategy=strategy)
    assert query_params.strategy == strategy


def test_device_strategy_query_params_invalid_strategy() -> None:
    strategy: list[str] = ["invalid-strategy"]
    with pytest.raises(HTTPException) as e:
        strategy = DeviceStrategyQueryParams(strategy=strategy)  # type: ignore
        assert e.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # type: ignore
        assert e.detail == "Invalid device strategy, must be 'mobile' or 'desktop'"  # type: ignore  # noqa: E501


def test_device_strategy_query_params_none() -> None:
    query_params = DeviceStrategyQueryParams()
    assert query_params.strategy is None


def test_public_query_params() -> None:
    message = "Hello, world!"
    query_params = PublicQueryParams(message=message)
    assert query_params.message == message

    query_params = PublicQueryParams()
    assert query_params.message is None

    query_params = PublicQueryParams(message=None)
    assert query_params.message is None


def test_ga4_property_id_query_params_valid_id() -> None:
    uuid_1 = get_uuid_str()
    query_params = Ga4QueryParams(ga4_id=uuid_1)
    assert query_params.ga4_id == uuid.UUID(uuid_1)


def test_ga4_property_id_query_params_invalid_id() -> None:
    fake_id = "invalid-id"
    try:
        Ga4QueryParams(ga4_id=fake_id)
    except HTTPException as e:
        assert e.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert e.detail == "Invalid ga4 property ID"


def test_ga4_property_id_query_params_none() -> None:
    query_params = Ga4QueryParams()
    assert query_params.ga4_id is None


def test_common_user_query_params() -> None:
    uuid_1 = get_uuid_str()
    query_params = CommonUserQueryParams(page=2, size=10, user_id=uuid_1)
    assert query_params.page == 2
    assert query_params.size == 10
    assert query_params.user_id == uuid.UUID(uuid_1)


def test_common_client_query_params() -> None:
    uuid_1 = get_uuid_str()
    query_params = CommonClientQueryParams(page=2, size=10, client_id=uuid_1)
    assert query_params.page == 2
    assert query_params.size == 10
    assert query_params.client_id == uuid.UUID(uuid_1)

    query_params = CommonClientQueryParams()
    assert query_params.page == 1
    assert query_params.size == 1000
    assert query_params.client_id is None

    query_params = CommonClientQueryParams(page=None, size=None, client_id=None)
    assert query_params.page == 1
    assert query_params.size == 1000
    assert query_params.client_id is None


def test_common_user_client_query_params() -> None:
    uuid_1 = get_uuid_str()
    uuid_2 = get_uuid_str()
    query_params = CommonUserClientQueryParams(
        page=2,
        size=10,
        user_id=uuid_1,
        client_id=uuid_2,
    )
    assert query_params.page == 2
    assert query_params.size == 10
    assert query_params.user_id == uuid.UUID(uuid_1)
    assert query_params.client_id == uuid.UUID(uuid_2)

    query_params = CommonUserClientQueryParams()
    assert query_params.page == 1
    assert query_params.size == 1000
    assert query_params.user_id is None
    assert query_params.client_id is None

    query_params = CommonUserClientQueryParams(
        page=None, size=None, user_id=None, client_id=None
    )
    assert query_params.page == 1
    assert query_params.size == 1000
    assert query_params.user_id is None
    assert query_params.client_id is None


def test_common_website_query_params() -> None:
    uuid_1 = get_uuid_str()
    query_params = CommonWebsiteQueryParams(page=2, size=10, website_id=uuid_1)
    assert query_params.page == 2
    assert query_params.size == 10
    assert query_params.website_id == uuid.UUID(uuid_1)

    query_params = CommonWebsiteQueryParams()
    assert query_params.page == 1
    assert query_params.size == 1000
    assert query_params.website_id is None

    query_params = CommonWebsiteQueryParams(page=None, size=None, website_id=None)
    assert query_params.page == 1
    assert query_params.size == 1000
    assert query_params.website_id is None


def test_common_client_website_query_params() -> None:
    uuid_1 = get_uuid_str()
    uuid_2 = get_uuid_str()
    query_params = CommonClientWebsiteQueryParams(
        page=2,
        size=10,
        client_id=uuid_1,
        website_id=uuid_2,
    )
    assert query_params.page == 2
    assert query_params.size == 10
    assert query_params.client_id == uuid.UUID(uuid_1)
    assert query_params.website_id == uuid.UUID(uuid_2)

    query_params = CommonClientWebsiteQueryParams()
    assert query_params.page == 1
    assert query_params.size == settings.api.query_limit_rows_default
    assert query_params.client_id is None
    assert query_params.website_id is None

    query_params = CommonClientWebsiteQueryParams(
        page=None, size=None, client_id=None, website_id=None
    )
    assert query_params.page == 1
    assert query_params.size == settings.api.query_limit_rows_default
    assert query_params.client_id is None
    assert query_params.website_id is None


def test_common_website_page_query_params() -> None:
    uuid_1 = get_uuid_str()
    uuid_2 = get_uuid_str()
    query_params = CommonWebsitePageQueryParams(
        page=2,
        size=10,
        website_id=uuid_1,
        sitemap_id=uuid_2,
    )
    assert query_params.page == 2
    assert query_params.size == 10
    assert query_params.website_id == uuid.UUID(uuid_1)
    assert query_params.sitemap_id == uuid.UUID(uuid_2)

    query_params = CommonWebsitePageQueryParams()
    assert query_params.page == 1
    assert query_params.size == settings.api.query_limit_rows_default
    assert query_params.website_id is None
    assert query_params.sitemap_id is None

    query_params = CommonWebsitePageQueryParams(
        page=None, size=None, website_id=None, sitemap_id=None
    )
    assert query_params.page == 1
    assert query_params.size == settings.api.query_limit_rows_default
    assert query_params.website_id is None
    assert query_params.sitemap_id is None


def test_common_website_map_query_params() -> None:
    uuid_1 = get_uuid_str()
    query_params = CommonWebsiteMapQueryParams(
        page=2,
        size=10,
        website_id=uuid_1,
    )
    assert query_params.page == 2
    assert query_params.size == 10
    assert query_params.website_id == uuid.UUID(uuid_1)

    query_params = CommonWebsiteMapQueryParams()
    assert query_params.page == 1
    assert query_params.size == settings.api.query_limit_rows_default
    assert query_params.website_id is None

    query_params = CommonWebsiteMapQueryParams(page=None, size=None, website_id=None)
    assert query_params.page == 1
    assert query_params.size == settings.api.query_limit_rows_default
    assert query_params.website_id is None


def test_common_website_page_speed_insights_query_params() -> None:
    uuid_1 = get_uuid_str()
    uuid_2 = get_uuid_str()
    query_params = CommonWebsitePageSpeedInsightsQueryParams(
        page=2,
        size=10,
        website_id=uuid_1,
        page_id=uuid_2,
        strategy=["desktop", "mobile"],
    )
    assert query_params.page == 2
    assert query_params.size == 10
    assert query_params.website_id == uuid.UUID(uuid_1)
    assert query_params.page_id == uuid.UUID(uuid_2)
    assert query_params.strategy == ["desktop", "mobile"]

    query_params = CommonWebsitePageSpeedInsightsQueryParams()
    assert query_params.page == 1
    assert query_params.size == settings.api.query_limit_rows_default
    assert query_params.website_id is None
    assert query_params.page_id is None
    assert query_params.strategy is None

    query_params = CommonWebsitePageSpeedInsightsQueryParams(
        page=None, size=None, website_id=None, page_id=None, strategy=None
    )
    assert query_params.page == 1
    assert query_params.size == settings.api.query_limit_rows_default
    assert query_params.website_id is None
    assert query_params.page_id is None
    assert query_params.strategy is None


def test_common_website_keyword_corpus_query_params() -> None:
    uuid_1 = get_uuid_str()
    uuid_2 = get_uuid_str()
    query_params = CommonWebsiteKeywordCorpusQueryParams(
        page=2,
        size=10,
        website_id=uuid_1,
        page_id=uuid_2,
    )
    assert query_params.page == 2
    assert query_params.size == 10
    assert query_params.website_id == uuid.UUID(uuid_1)
    assert query_params.page_id == uuid.UUID(uuid_2)

    query_params = CommonWebsiteKeywordCorpusQueryParams()
    assert query_params.page == 1
    assert query_params.size == settings.api.query_limit_rows_default
    assert query_params.website_id is None
    assert query_params.page_id is None

    query_params = CommonWebsiteKeywordCorpusQueryParams(
        page=None, size=None, website_id=None, page_id=None
    )
    assert query_params.page == 1
    assert query_params.size == settings.api.query_limit_rows_default
    assert query_params.website_id is None
    assert query_params.page_id is None


def test_common_ga4_query_params() -> None:
    uuid_1 = get_uuid_str()
    uuid_2 = get_uuid_str()
    query_params = CommonWebsiteGa4QueryParams(
        page=2,
        size=5,
        website_id=uuid_1,
        ga4_id=uuid_2,
    )
    assert query_params.page == 2
    assert query_params.size == 5
    assert query_params.website_id == uuid.UUID(uuid_1)
    assert query_params.ga4_id == uuid.UUID(uuid_2)

    query_params = CommonWebsiteGa4QueryParams()
    assert query_params.page == 1
    assert query_params.size == settings.api.query_limit_rows_default
    assert query_params.website_id is None
    assert query_params.ga4_id is None

    query_params = CommonWebsiteGa4QueryParams(
        page=None, size=None, website_id=None, ga4_id=None
    )
    assert query_params.page == 1
    assert query_params.size == settings.api.query_limit_rows_default
    assert query_params.website_id is None
    assert query_params.ga4_id is None


def test_date_start_query_params() -> None:
    query_1 = DateStartQueryParams(date_start="2021-01-01")
    assert query_1.date_start == dt.date.fromisoformat("2021-01-01")
    query_2 = DateStartQueryParams(date_start="2024-01-01")
    assert query_2.date_start == dt.date.fromisoformat("2024-01-01")
    query_3 = DateStartQueryParams(date_start=None)
    assert query_3.date_start is None
    with pytest.raises(HTTPException) as e:
        DateStartQueryParams(date_start="invalid")
        assert e.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # type: ignore
        assert e.detail == "Invalid date start"  # type: ignore


def test_date_end_query_params() -> None:
    query_1 = DateEndQueryParams(date_end="2021-01-01")
    assert query_1.date_end == dt.date.fromisoformat("2021-01-01")
    query_2 = DateEndQueryParams(date_end="2024-01-01")
    assert query_2.date_end == dt.date.fromisoformat("2024-01-01")
    query_3 = DateEndQueryParams(date_end=None)
    assert query_3.date_end is None
    with pytest.raises(HTTPException) as e:
        DateEndQueryParams(date_end="invalid")
        assert e.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # type: ignore
        assert e.detail == "Invalid date end"  # type: ignore


def test_gsc_metric_types_query_params() -> None:
    metric_types = "page,query"
    query_metric_types_none = GoSearchConsoleMetricTypeQueryParams(metric_types=None)
    assert query_metric_types_none.metric_types is None
    query_metric_types = GoSearchConsoleMetricTypeQueryParams(metric_types=metric_types)
    assert query_metric_types.metric_types == [
        GoSearchConsoleMetricType.page,
        GoSearchConsoleMetricType.query,
    ]
    with pytest.raises(GoSearchConsoleMetricTypeInvalid):
        GoSearchConsoleMetricTypeQueryParams(metric_types="invalid")


def test_common_go_sc_query_params() -> None:
    query_1 = CommonWebsiteGoSearchConsoleQueryParams(
        1, 100, "page,query", "2021-01-01", "2021-01-31"
    )
    assert query_1.page == 1
    assert query_1.size == 100
    assert query_1.metric_types == [
        GoSearchConsoleMetricType.page,
        GoSearchConsoleMetricType.query,
    ]
