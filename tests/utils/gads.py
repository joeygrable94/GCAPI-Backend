from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GoAdsPropertyRepository
from app.db.constants import DB_STR_16BIT_MAXLEN_INPUT
from app.models import GoAdsProperty
from app.schemas import GoAdsPropertyCreate, GoAdsPropertyRead
from tests.utils.utils import random_lower_string


async def create_random_go_ads_property(
    db_session: AsyncSession, client_id: UUID4, platform_id: UUID4
) -> GoAdsPropertyRead:
    repo: GoAdsPropertyRepository = GoAdsPropertyRepository(session=db_session)
    go_ads_property: GoAdsProperty = await repo.create(
        schema=GoAdsPropertyCreate(
            title=random_lower_string(chars=DB_STR_16BIT_MAXLEN_INPUT),
            measurement_id=random_lower_string(chars=DB_STR_16BIT_MAXLEN_INPUT),
            client_id=client_id,
            platform_id=platform_id,
        )
    )
    return GoAdsPropertyRead.model_validate(go_ads_property)
