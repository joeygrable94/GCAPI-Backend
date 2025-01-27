"""
Package Source:
https://github.com/jayhawk24/pagination-fastapi/tree/main

Asyncio Support Example:
https://github.com/dialoguemd/fastapi-sqla/blob/master/fastapi_sqla/asyncio_support.py

"""

from .core import (
    GetPaginatedQueryParams,
    PageParams,
    PageParamsFromQuery,
    Paginated,
    paginated_query,
)

__all__: list[str] = [
    "PageParams",
    "PageParamsFromQuery",
    "GetPaginatedQueryParams",
    "Paginated",
    "paginated_query",
]
