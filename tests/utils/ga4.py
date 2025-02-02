from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_16BIT_MAXLEN_INPUT
from app.entities.go_ga4.crud import GoAnalytics4PropertyRepository
from app.entities.go_ga4.model import GoAnalytics4Property
from app.entities.go_ga4.schemas import (
    GoAnalytics4PropertyCreate,
    GoAnalytics4PropertyRead,
)
from app.entities.go_ga4_stream.crud import GoAnalytics4StreamRepository
from app.entities.go_ga4_stream.model import GoAnalytics4Stream
from app.entities.go_ga4_stream.schemas import (
    GoAnalytics4StreamCreate,
    GoAnalytics4StreamRead,
)
from tests.utils.utils import random_lower_string


async def create_random_ga4_property(
    db_session: AsyncSession, client_id: UUID4, platform_id: UUID4
) -> GoAnalytics4PropertyRead:
    repo: GoAnalytics4PropertyRepository = GoAnalytics4PropertyRepository(
        session=db_session
    )
    ga4_property: GoAnalytics4Property = await repo.create(
        schema=GoAnalytics4PropertyCreate(
            title=random_lower_string(chars=DB_STR_16BIT_MAXLEN_INPUT),
            property_id=random_lower_string(chars=DB_STR_16BIT_MAXLEN_INPUT),
            client_id=client_id,
            platform_id=platform_id,
        )
    )
    return GoAnalytics4PropertyRead.model_validate(ga4_property)


async def create_random_ga4_stream(
    db_session: AsyncSession, ga4_id: UUID4, website_id: UUID4
) -> GoAnalytics4StreamRead:
    repo: GoAnalytics4StreamRepository = GoAnalytics4StreamRepository(
        session=db_session
    )
    ga4_stream: GoAnalytics4Stream = await repo.create(
        schema=GoAnalytics4StreamCreate(
            title=random_lower_string(chars=DB_STR_16BIT_MAXLEN_INPUT),
            stream_id=random_lower_string(chars=DB_STR_16BIT_MAXLEN_INPUT),
            measurement_id=random_lower_string(chars=DB_STR_16BIT_MAXLEN_INPUT),
            ga4_id=ga4_id,
            website_id=website_id,
        )
    )
    return GoAnalytics4StreamRead.model_validate(ga4_stream)
