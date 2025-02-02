from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_64BIT_MAXLEN_INPUT
from app.entities.go_gsc.crud import GoSearchConsolePropertyRepository
from app.entities.go_gsc.model import GoSearchConsoleProperty
from app.entities.go_gsc.schemas import (
    GoSearchConsolePropertyCreate,
    GoSearchConsolePropertyRead,
)
from tests.utils.utils import random_lower_string


async def create_random_go_search_console_property(
    db_session: AsyncSession, client_id: UUID4, website_id: UUID4, platform_id: UUID4
) -> GoSearchConsolePropertyRead:
    repo: GoSearchConsolePropertyRepository = GoSearchConsolePropertyRepository(
        session=db_session
    )
    go_sc: GoSearchConsoleProperty = await repo.create(
        schema=GoSearchConsolePropertyCreate(
            title=random_lower_string(chars=DB_STR_64BIT_MAXLEN_INPUT),
            client_id=client_id,
            platform_id=platform_id,
            website_id=website_id,
        )
    )
    return GoSearchConsolePropertyRead.model_validate(go_sc)
