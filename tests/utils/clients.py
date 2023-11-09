from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string

from app.crud import ClientRepository
from app.models import Client
from app.schemas import ClientCreate
from app.schemas import ClientRead


async def create_random_client(db_session: AsyncSession) -> ClientRead:
    repo: ClientRepository = ClientRepository(session=db_session)
    user: Client = await repo.create(
        schema=ClientCreate(
            title=random_lower_string(), description=random_lower_string()
        )
    )
    return ClientRead.model_validate(user)
