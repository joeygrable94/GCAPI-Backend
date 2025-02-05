from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from app.core.exceptions import get_global_headers
from app.entities.organization.errors import (
    OrganizationAlreadyExists,
    OrganizationNotFound,
    OrganizationRelationshipNotFound,
)


def configure_organization_exceptions(app: FastAPI) -> None:
    @app.exception_handler(OrganizationAlreadyExists)
    async def organization_already_exists_exception_handler(
        request: Request, exc: OrganizationAlreadyExists
    ) -> Response:
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(OrganizationNotFound)
    async def organization_not_found_exception_handler(
        request: Request, exc: OrganizationNotFound
    ) -> Response:
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )

    @app.exception_handler(OrganizationRelationshipNotFound)
    async def organization_relationship_not_found_exception_handler(
        request: Request, exc: OrganizationRelationshipNotFound
    ) -> Response:
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )
