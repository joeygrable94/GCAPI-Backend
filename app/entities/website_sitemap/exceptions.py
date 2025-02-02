from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from app.core.exceptions import get_global_headers
from app.entities.website_sitemap.errors import XmlInvalid


def configure_website_sitemap_exceptions(app: FastAPI) -> None:
    @app.exception_handler(XmlInvalid)
    async def xml_invalid_exception_handler(
        request: Request, exc: XmlInvalid
    ) -> Response:
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers={**get_global_headers()},
            ),
        )
