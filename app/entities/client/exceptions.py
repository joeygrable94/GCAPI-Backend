from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from app.core.exceptions import get_global_headers
from app.entities.client.errors import (
    ClientAlreadyExists,
    ClientNotFound,
    ClientRelationshipNotFound,
)


def configure_client_exceptions(app: FastAPI) -> None:
    @app.exception_handler(ClientAlreadyExists)
    async def client_already_exists_exception_handler(
        request: Request, exc: ClientAlreadyExists
    ) -> Response:
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
    ) -> Response:
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
    ) -> Response:
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )
