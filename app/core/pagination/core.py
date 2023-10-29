from typing import Generic, List, Sequence, Type, TypeVar

from pydantic import BaseModel, Field
from sqlalchemy import Result, Select, column, func, select, table
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings


class PageParams(BaseModel):
    page: int = Field(1, description="Page Number", ge=1)
    size: int = Field(
        settings.api.query_limit_rows_default,
        description="Page Size",
        ge=1,
        le=settings.api.query_limit_rows_max,
    )


T = TypeVar("T")


class Paginated(BaseModel, Generic[T]):
    """Response schema for any paged API."""

    total: int
    page: int
    size: int
    results: List[T]


async def paginated_query(
    table_name: str,
    db: AsyncSession,
    stmt: Select,
    page_params: PageParams,
    response_schema: Type[BaseModel],
) -> Paginated[T]:
    """Paginate the query."""
    count_table = table(table_name, column("id"))
    count_stmt: Select = select(func.count()).select_from(count_table)
    count_rslt: Result = await db.execute(count_stmt)
    total_count: Sequence = count_rslt.scalars().all()

    paginated_query = stmt.offset((page_params.page - 1) * page_params.size).limit(
        page_params.size
    )
    result: Result = await db.execute(paginated_query)
    data: Sequence = result.scalars().all()

    return Paginated(
        total=len(total_count),
        page=page_params.page,
        size=page_params.size,
        results=[response_schema.model_validate(item) for item in data],
    )
