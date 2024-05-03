from typing import Dict, List

from asgi_correlation_id.context import correlation_id
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler

from .errors import ErrorCode, ErrorCodeReasonModel, ErrorModel
from .exceptions import (
    ApiException,
    BdxFeedAlreadyExists,
    BdxFeedNotExists,
    ClientAlreadyExists,
    ClientNotExists,
    ClientRelationshipNotExists,
    ClientReportAlreadyExists,
    ClientReportNotExists,
    Ga4PropertyAlreadyExists,
    Ga4PropertyNotExists,
    Ga4StreamAlreadyExists,
    Ga4StreamNotExists,
    GoCloudPropertyAlreadyExists,
    GoCloudPropertyNotExists,
    GoSearchConsoleMetricNotExists,
    GoSearchConsoleMetricTypeInvalid,
    GoSearchConsolePropertyAlreadyExists,
    GoSearchConsolePropertyNotExists,
    InvalidID,
    NoteAlreadyExists,
    NoteNotExists,
    SharpspringAlreadyExists,
    SharpspringNotExists,
    UserAlreadyExists,
    UserNotExists,
    WebsiteAlreadyExists,
    WebsiteDomainInvalid,
    WebsiteMapAlreadyExists,
    WebsiteMapNotExists,
    WebsiteMapUrlXmlInvalid,
    WebsiteNotExists,
    WebsitePageAlreadyExists,
    WebsitePageKeywordCorpusNotExists,
    WebsitePageNotExists,
    WebsitePageSpeedInsightsNotExists,
)


def get_global_headers(inject_headers: Dict[str, str] | None = None) -> Dict[str, str]:
    global_headers = {
        "x-request-id": correlation_id.get() or "",
        "Access-Control-Expose-Headers": "x-request-id",
    }
    if inject_headers is not None:
        global_headers.update(inject_headers)  # pragma: no cover
    return global_headers


def configure_exceptions(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> Response:
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal server error",
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(ApiException)
    async def api_exception_exception_handler(
        request: Request, exc: ApiException
    ) -> Response:  # noqa: E501
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(InvalidID)
    async def invalid_id_exception_handler(
        request: Request, exc: InvalidID
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(UserAlreadyExists)
    async def user_already_exists_exception_handler(
        request: Request, exc: UserAlreadyExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(UserNotExists)
    async def user_not_exists_exception_handler(
        request: Request, exc: UserNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(ClientAlreadyExists)
    async def client_already_exists_exception_handler(
        request: Request, exc: ClientAlreadyExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(ClientNotExists)
    async def client_not_exists_exception_handler(
        request: Request, exc: ClientNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(ClientRelationshipNotExists)
    async def client_relationship_not_exists_exception_handler(
        request: Request, exc: ClientRelationshipNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(ClientReportAlreadyExists)
    async def client_report_already_exists_exception_handler(
        request: Request, exc: ClientReportAlreadyExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(ClientReportNotExists)
    async def client_report_not_exists_exception_handler(
        request: Request, exc: ClientReportNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(NoteAlreadyExists)
    async def note_already_exists_exception_handler(
        request: Request, exc: NoteAlreadyExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(NoteNotExists)
    async def note_not_exists_exception_handler(
        request: Request, exc: NoteNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(WebsiteAlreadyExists)
    async def website_already_exists_exception_handler(
        request: Request, exc: WebsiteAlreadyExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(WebsiteNotExists)
    async def website_not_exists_exception_handler(
        request: Request, exc: WebsiteNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(WebsiteDomainInvalid)
    async def website_domain_invalid_exception_handler(
        request: Request, exc: WebsiteDomainInvalid
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(WebsiteMapAlreadyExists)
    async def website_map_already_exists_exception_handler(
        request: Request, exc: WebsiteMapAlreadyExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(WebsiteMapNotExists)
    async def website_map_not_exists_exception_handler(
        request: Request, exc: WebsiteMapNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(WebsiteMapUrlXmlInvalid)
    async def website_map_url_xml_invalid_exception_handler(
        request: Request, exc: WebsiteMapUrlXmlInvalid
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(WebsitePageAlreadyExists)
    async def website_page_already_exists_exception_handler(
        request: Request, exc: WebsitePageAlreadyExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(WebsitePageNotExists)
    async def website_page_not_exists_exception_handler(
        request: Request, exc: WebsitePageNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(WebsitePageSpeedInsightsNotExists)
    async def website_page_speed_insights_not_exists_exception_handler(
        request: Request, exc: WebsitePageSpeedInsightsNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(WebsitePageKeywordCorpusNotExists)
    async def website_page_keyword_corpus_not_exists_exception_handler(
        request: Request, exc: WebsitePageKeywordCorpusNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(BdxFeedNotExists)
    async def bdx_feed_not_exists_exception_handler(
        request: Request, exc: BdxFeedNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(BdxFeedAlreadyExists)
    async def bdx_feed_already_exists_exception_handler(
        request: Request, exc: BdxFeedAlreadyExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(SharpspringNotExists)
    async def sharpspring_not_exists_exception_handler(
        request: Request, exc: SharpspringNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(SharpspringAlreadyExists)
    async def sharpspring_already_exists_exception_handler(
        request: Request, exc: SharpspringAlreadyExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(GoCloudPropertyNotExists)
    async def go_cloud_not_exists_exception_handler(
        request: Request, exc: GoCloudPropertyNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(GoCloudPropertyAlreadyExists)
    async def go_cloud_already_exists_exception_handler(
        request: Request, exc: GoCloudPropertyAlreadyExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(Ga4PropertyNotExists)
    async def ga4_property_not_exists_exception_handler(
        request: Request, exc: Ga4PropertyNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(Ga4PropertyAlreadyExists)
    async def ga4_property_already_exists_exception_handler(
        request: Request, exc: Ga4PropertyAlreadyExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(Ga4StreamNotExists)
    async def ga4_stream_not_exists_exception_handler(
        request: Request, exc: Ga4PropertyNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(Ga4StreamAlreadyExists)
    async def ga4_stream_already_exists_exception_handler(
        request: Request, exc: Ga4PropertyAlreadyExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(GoSearchConsolePropertyAlreadyExists)
    async def go_search_console_property_already_exists_exception_handler(
        request: Request, exc: GoSearchConsolePropertyAlreadyExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(GoSearchConsolePropertyNotExists)
    async def go_search_console_property_not_exists_exception_handler(
        request: Request, exc: GoSearchConsolePropertyNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(GoSearchConsoleMetricTypeInvalid)
    async def go_search_console_metric_type_invalid_exception_handler(
        request: Request, exc: GoSearchConsoleMetricTypeInvalid
    ) -> Response:  # noqa: E501  # pragma: no cover
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(GoSearchConsoleMetricNotExists)
    async def go_search_console_metric_not_exists_exception_handler(
        request: Request, exc: GoSearchConsoleMetricNotExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )


__all__: List[str] = [
    "ApiException",
    "ClientAlreadyExists",
    "ClientNotExists",
    "ClientRelationshipNotExists",
    "ClientReportAlreadyExists",
    "ClientReportNotExists",
    "configure_exceptions",
    "ErrorModel",
    "ErrorCodeReasonModel",
    "ErrorCode",
    "InvalidID",
    "NoteAlreadyExists",
    "NoteNotExists",
    "UserAlreadyExists",
    "UserNotExists",
    "WebsiteAlreadyExists",
    "WebsiteNotExists",
    "WebsiteDomainInvalid",
    "WebsiteMapAlreadyExists",
    "WebsiteMapNotExists",
    "WebsitePageAlreadyExists",
    "WebsitePageNotExists",
    "WebsitePageSpeedInsightsNotExists",
    "WebsitePageKeywordCorpusNotExists",
    "BdxFeedNotExists",
    "BdxFeedAlreadyExists",
    "SharpspringNotExists",
    "SharpspringAlreadyExists",
    "GoCloudPropertyNotExists",
    "GoCloudPropertyAlreadyExists",
    "Ga4PropertyNotExists",
    "Ga4PropertyAlreadyExists",
    "Ga4StreamNotExists",
    "Ga4StreamAlreadyExists",
    "GoSearchConsolePropertyAlreadyExists",
    "GoSearchConsolePropertyNotExists",
    "GoSearchConsoleMetricTypeInvalid",
    "GoSearchConsoleMetricNotExists",
]
