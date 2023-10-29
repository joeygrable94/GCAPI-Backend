"""
Package Source:
https://github.com/jayhawk24/pagination-fastapi/tree/main

Asyncio Support Example:
https://github.com/dialoguemd/fastapi-sqla/blob/master/fastapi_sqla/asyncio_support.py

"""

from typing import List

from .core import PageParams, Paginated, paginated_query

__all__: List[str] = [
    "PageParams",
    "Paginated",
    "paginated_query",
]
