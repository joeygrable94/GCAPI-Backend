from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import (
    random_datetime,
    random_float,
    random_integer,
    random_lower_string,
)

from app.crud import GoSearchConsoleMetricRepository, GoSearchConsolePropertyRepository
from app.db.constants import DB_STR_64BIT_MAXLEN_INPUT
from app.models import (
    GoSearchConsoleCountry,
    GoSearchConsoleDevice,
    GoSearchConsolePage,
    GoSearchConsoleProperty,
    GoSearchConsoleQuery,
    GoSearchConsoleSearchappearance,
)
from app.schemas import (
    GoSearchConsoleMetricCreate,
    GoSearchConsoleMetricRead,
    GoSearchConsoleMetricType,
    GoSearchConsolePropertyCreate,
    GoSearchConsolePropertyRead,
)


async def create_random_go_search_console_property(
    db_session: AsyncSession, client_id: UUID4, website_id: UUID4
) -> GoSearchConsolePropertyRead:
    repo: GoSearchConsolePropertyRepository = GoSearchConsolePropertyRepository(
        session=db_session
    )
    go_sc: GoSearchConsoleProperty = await repo.create(
        schema=GoSearchConsolePropertyCreate(
            title=random_lower_string(chars=DB_STR_64BIT_MAXLEN_INPUT),
            client_id=client_id,
            website_id=website_id,
        )
    )
    return GoSearchConsolePropertyRead.model_validate(go_sc)


async def create_random_go_search_console_property_metric(
    db_session: AsyncSession, gsc_id: UUID4, metric_type: GoSearchConsoleMetricType
) -> GoSearchConsoleMetricRead:
    repo = GoSearchConsoleMetricRepository(session=db_session, metric_type=metric_type)
    gsc_metric: (
        GoSearchConsoleSearchappearance
        | GoSearchConsoleQuery
        | GoSearchConsolePage
        | GoSearchConsoleDevice
        | GoSearchConsoleCountry
    ) = await repo.create(
        schema=GoSearchConsoleMetricCreate(
            title=random_lower_string(chars=DB_STR_64BIT_MAXLEN_INPUT),
            keys=random_lower_string(),
            clicks=random_integer(),
            impressions=random_integer(),
            ctr=random_float(),
            position=random_float(),
            date_start=random_datetime(),
            date_end=random_datetime(),
            gsc_id=gsc_id,
        )
    )
    return GoSearchConsoleMetricRead.model_validate(gsc_metric)
