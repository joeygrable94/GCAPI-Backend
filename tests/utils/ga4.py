from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GoAnalytics4PropertyRepository, GoAnalytics4StreamRepository
from app.db.constants import DB_STR_16BIT_MAXLEN_INPUT
from app.models import GoAnalytics4Property, GoAnalytics4Stream
from app.schemas import (
    GoAnalytics4PropertyCreate,
    GoAnalytics4PropertyRead,
    GoAnalytics4StreamCreate,
    GoAnalytics4StreamRead,
)
from tests.utils.utils import random_lower_string


async def create_random_ga4_property(
    db_session: AsyncSession, client_id: UUID4
) -> GoAnalytics4PropertyRead:
    repo: GoAnalytics4PropertyRepository = GoAnalytics4PropertyRepository(
        session=db_session
    )
    ga4_property: GoAnalytics4Property = await repo.create(
        schema=GoAnalytics4PropertyCreate(
            title=random_lower_string(chars=DB_STR_16BIT_MAXLEN_INPUT),
            measurement_id=random_lower_string(chars=DB_STR_16BIT_MAXLEN_INPUT),
            property_id=random_lower_string(chars=DB_STR_16BIT_MAXLEN_INPUT),
            client_id=client_id,
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
            ga4_id=ga4_id,
            website_id=website_id,
        )
    )
    return GoAnalytics4StreamRead.model_validate(ga4_stream)
