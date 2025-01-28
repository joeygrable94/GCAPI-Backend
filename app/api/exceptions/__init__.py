from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler

from .errors import ErrorCode, ErrorCodeReasonModel, ErrorModel
from .exceptions import (
    ApiException,
    ClientAlreadyExists,
    ClientNotFound,
    ClientRelationshipNotFound,
    DomainInvalid,
    EntityAlreadyExists,
    EntityNotFound,
    EntityRelationshipNotFound,
    InvalidID,
    UserAlreadyExists,
    UserNotFound,
    XmlInvalid,
)


def get_global_headers(inject_headers: dict[str, str] | None = None) -> dict[str, str]:
    global_headers = {
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
        return await http_exception_handler(  # pragma: no cover
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
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(UserNotFound)
    async def user_not_found_exception_handler(
        request: Request, exc: UserNotFound
    ) -> Response:  # noqa: E501
        return await http_exception_handler(  # pragma: no cover
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
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(ClientNotFound)
    async def client_not_found_exception_handler(
        request: Request, exc: ClientNotFound
    ) -> Response:  # noqa: E501
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(ClientRelationshipNotFound)
    async def client_relationship_not_found_exception_handler(
        request: Request, exc: ClientRelationshipNotFound
    ) -> Response:  # noqa: E501
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(XmlInvalid)
    async def xml_invalid_exception_handler(
        request: Request, exc: XmlInvalid
    ) -> Response:  # noqa: E501
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(DomainInvalid)
    async def domain_invalid_exception_handler(
        request: Request, exc: DomainInvalid
    ) -> Response:  # noqa: E501
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(EntityAlreadyExists)
    async def entity_already_exists_exception_handler(
        request: Request, exc: EntityAlreadyExists
    ) -> Response:  # noqa: E501
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(EntityNotFound)
    async def entity_not_found_exception_handler(
        request: Request, exc: EntityNotFound
    ) -> Response:  # noqa: E501
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(EntityRelationshipNotFound)
    async def entity_relationship_not_found_exception_handler(
        request: Request, exc: EntityRelationshipNotFound
    ) -> Response:  # noqa: E501
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )


__all__: list[str] = [
    "ApiException",
    "ClientAlreadyExists",
    "ClientNotFound",
    "ClientRelationshipNotFound",
    "configure_exceptions",
    "ErrorModel",
    "ErrorCodeReasonModel",
    "ErrorCode",
    "InvalidID",
    "UserAlreadyExists",
    "UserNotFound",
    "EntityAlreadyExists",
    "EntityNotFound",
    "EntityRelationshipNotFound",
    "DomainInvalid",
    "XmlInvalid",
]
