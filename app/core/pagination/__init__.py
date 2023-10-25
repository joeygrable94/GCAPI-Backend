# https://github.com/jayhawk24/pagination-fastapi/tree/main
from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from sqlalchemy.orm import Query


class PageParams(BaseModel):
    page: int = Field(1, description="Page number", ge=1)
    size: int = Field(10, description="Page size", ge=1, le=100)


T = TypeVar("T")


class PagedResponseSchema(GenericModel, Generic[T]):
    """Response schema for any paged API."""

    total: int
    page: int
    size: int
    results: List[T]


def paginate(
    page_params: PageParams, query: Query, ResponseSchema: BaseModel
) -> PagedResponseSchema[T]:
    """Paginate the query."""
    paginated_query = (
        query.offset((page_params.page - 1) * page_params.size)
        .limit(page_params.size)
        .all()
    )

    return PagedResponseSchema(
        total=query.count(),
        page=page_params.page,
        size=page_params.size,
        results=[ResponseSchema.from_orm(item) for item in paginated_query],
    )
