import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import GoSearchConsoleMetricTypeInvalid
from app.crud import GoSearchConsoleMetricRepository
from app.models import GoSearchConsoleQuery
from app.schemas import GoSearchConsoleMetricType

pytestmark = pytest.mark.asyncio


async def test_go_sc_query_repo_table(db_session: AsyncSession) -> None:
    valid_metric_type = GoSearchConsoleMetricType.query
    repo: GoSearchConsoleMetricRepository = GoSearchConsoleMetricRepository(
        session=db_session,
        metric_type=valid_metric_type,
    )
    assert repo._table is GoSearchConsoleQuery

    with pytest.raises(GoSearchConsoleMetricTypeInvalid):
        GoSearchConsoleMetricRepository(session=db_session)

    with pytest.raises(GoSearchConsoleMetricTypeInvalid):
        GoSearchConsoleMetricRepository(session=db_session, metric_type="invalid_type")
