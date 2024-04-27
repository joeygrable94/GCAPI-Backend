from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string

from app.crud import SharpspringRepository
from app.models import Sharpspring
from app.schemas import SharpspringCreate, SharpspringRead


async def create_random_sharpspring(
    db_session: AsyncSession, client_id: UUID4
) -> SharpspringRead:
    repo: SharpspringRepository = SharpspringRepository(session=db_session)
    sharpspring: Sharpspring = await repo.create(
        schema=SharpspringCreate(
            api_key=random_lower_string(chars=64),
            secret_key=random_lower_string(chars=64),
            client_id=client_id,
        )
    )
    return SharpspringRead.model_validate(sharpspring)
