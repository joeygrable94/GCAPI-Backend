from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler
from pydantic_core import ValidationError

from app.core.exceptions import ApiException, get_global_headers
from app.entities.api.constants import ERROR_MESSAGE_INPUT_SCHEMA_INVALID
from app.entities.api.errors import (
    EntityAlreadyExists,
    EntityNotFound,
    EntityRelationshipNotFound,
    InvalidID,
)


def configure_api_exceptions(app: FastAPI) -> None:
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
    ) -> Response:
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(ValidationError)
    async def pydantic_model_validation_exception_handler(
        request: Request, exc: ValidationError
    ) -> Response:
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=ERROR_MESSAGE_INPUT_SCHEMA_INVALID,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(InvalidID)
    async def invalid_id_exception_handler(
        request: Request, exc: InvalidID
    ) -> Response:
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
    ) -> Response:
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
    ) -> Response:
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
    ) -> Response:
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )
