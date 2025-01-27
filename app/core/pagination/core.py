from collections.abc import Sequence
from typing import Annotated, Generic, TypeVar

from fastapi import Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import Result, Select, TableClause, func, table
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import column as sql_column
from sqlalchemy.sql import select as sql_select

from app.core.config import settings

PAGE_SIZE_MAX = settings.api.query_limit_rows_max
PAGE_SIZE_DEFAULT = settings.api.query_limit_rows_default


class PageParamsFromQuery:
    def __init__(
        self,
        page: Annotated[int | None, Query(ge=1)] = 1,
        size: Annotated[
            int | None,
            Query(
                ge=1,
                le=PAGE_SIZE_MAX,
            ),
        ] = PAGE_SIZE_DEFAULT,
    ):
        page = 1 if page is None or page < 1 else page
        size = PAGE_SIZE_DEFAULT if size is None or size < 1 else size
        size = PAGE_SIZE_MAX if size > PAGE_SIZE_MAX else size
        self.page = page
        self.size = size


GetPaginatedQueryParams = Annotated[PageParamsFromQuery, Depends()]


class PageParams(BaseModel):
    page: int = Field(1, description="Page Number", ge=1)
    size: int = Field(
        PAGE_SIZE_DEFAULT,
        description="Page Size",
        ge=1,
        le=PAGE_SIZE_MAX,
    )


T = TypeVar("T", bound=BaseModel)


class Paginated(BaseModel, Generic[T]):
    """Response schema for any paged API."""

    total: int
    page: int
    size: int
    results: list[T]

    def __repr__(self) -> str:  # pragma: no cover
        return "<{} total={} page={} size={} results={}>".format(
            "Paginated",
            self.total,
            self.page,
            self.size,
            len(self.results),
        )


async def paginated_query(
    table_name: str,
    db: AsyncSession,
    stmt: Select,
    page_params: PageParams,
    response_schema: Generic[T],
) -> Paginated[T]:
    """Paginate the query."""
    count_table: TableClause
    count_stmt: Select
    total_count: int | None = None
    if stmt.whereclause is not None:
        # TODO: THIS IS A HACK TO GET THE COUNT
        # need to find a better way to get the count
        # without having to do a subquery
        total_query = stmt
        total_result = await db.execute(total_query)
        total_data = total_result.scalars().all()
        total_count = len(total_data)
    else:
        count_table = table(table_name, sql_column("id"))
        count_stmt = sql_select(func.count()).select_from(count_table)
        total_count = await db.scalar(count_stmt)

    paginated_query = stmt.offset((page_params.page - 1) * page_params.size).limit(
        page_params.size
    )
    result: Result = await db.execute(paginated_query)
    data: Sequence = result.scalars().all()

    return Paginated(
        total=total_count or 0,
        page=page_params.page,
        size=page_params.size,
        results=[response_schema.model_validate(item) for item in data],
    )
