from typing import Dict, List

from asgi_correlation_id.context import correlation_id
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler

from app.core.security import (
    Auth0UnauthenticatedException,
    Auth0UnauthorizedException,
    AuthPermissionException,
    CipherError,
    CsrfProtectError,
    RateLimitedRequestException,
)

from .errors import ErrorCode, ErrorCodeReasonModel, ErrorModel
from .exceptions import (
    ApiException,
    ClientAlreadyExists,
    ClientNotExists,
    EntityIdNotProvided,
    InvalidID,
    NoteAlreadyExists,
    NoteNotExists,
    UserAlreadyExists,
    UserNotExists,
    WebsiteAlreadyExists,
    WebsiteDomainInvalid,
    WebsiteMapAlreadyExists,
    WebsiteMapNotExists,
    WebsiteNotExists,
    WebsitePageAlreadyExists,
    WebsitePageKeywordCorpusAlreadyExists,
    WebsitePageKeywordCorpusNotExists,
    WebsitePageNotExists,
    WebsitePageSpeedInsightsAlreadyExists,
    WebsitePageSpeedInsightsNotExists,
)


def get_global_headers() -> Dict[str, str]:
    return {
        "x-request-id": correlation_id.get() or "",
        "Access-Control-Expose-Headers": "x-request-id",
    }


def configure_exceptions(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> Response:
        return await http_exception_handler(
            request,
            HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal server error",
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(CsrfProtectError)
    async def csrf_protect_exception_handler(
        request: Request, exc: CsrfProtectError
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(CipherError)
    async def rsa_security_exception_handler(
        request: Request, exc: CsrfProtectError
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(Auth0UnauthenticatedException)
    async def auth0_unauthenticated_exception_handler(
        request: Request, exc: Auth0UnauthenticatedException
    ) -> Response:  # noqa: E501
        request_headers = get_global_headers()
        if exc.headers:
            request_headers.update(exc.headers)
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.detail,
                headers=request_headers,
            ),
        )

    @app.exception_handler(Auth0UnauthorizedException)
    async def auth0_unauthorized_exception_handler(
        request: Request, exc: Auth0UnauthorizedException
    ) -> Response:  # noqa: E501
        request_headers = get_global_headers()
        if exc.headers:
            request_headers.update(exc.headers)
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.detail,
                headers=request_headers,
            ),
        )

    @app.exception_handler(AuthPermissionException)
    async def permissions_exception_handler(
        request: Request, exc: AuthPermissionException
    ) -> Response:  # noqa: E501
        request_headers = get_global_headers()
        if exc.headers:
            request_headers.update(exc.headers)
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers=request_headers,
            ),
        )

    @app.exception_handler(RateLimitedRequestException)
    async def rate_limited_request_exception_handler(
        request: Request, exc: RateLimitedRequestException
    ) -> Response:  # noqa: E501
        request_headers = get_global_headers()
        if exc.headers:
            request_headers.update(exc.headers)
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers=request_headers,
            ),
        )

    @app.exception_handler(ApiException)
    async def api_exception_exception_handler(
        request: Request, exc: ApiException
    ) -> Response:  # noqa: E501
        return await http_exception_handler(
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

    @app.exception_handler(EntityIdNotProvided)
    async def entity_id_not_provided_exception_handler(
        request: Request, exc: EntityIdNotProvided
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

    @app.exception_handler(WebsitePageSpeedInsightsAlreadyExists)
    async def website_page_speed_insights_already_exists_exception_handler(
        request: Request, exc: WebsitePageSpeedInsightsAlreadyExists
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

    @app.exception_handler(WebsitePageKeywordCorpusAlreadyExists)
    async def website_page_keyword_corpus_already_exists_exception_handler(
        request: Request, exc: WebsitePageKeywordCorpusAlreadyExists
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


__all__: List[str] = [
    "ApiException",
    "ClientAlreadyExists",
    "ClientNotExists",
    "configure_exceptions",
    "EntityIdNotProvided",
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
    "WebsitePageSpeedInsightsAlreadyExists",
    "WebsitePageSpeedInsightsNotExists",
    "WebsitePageKeywordCorpusAlreadyExists",
    "WebsitePageKeywordCorpusNotExists",
]
