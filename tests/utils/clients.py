from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string

from app.db.repositories import ClientsRepository
from app.db.schemas import ClientCreate, ClientRead
from app.db.tables import Client


async def create_random_client(db_session: AsyncSession) -> ClientRead:
    repo: ClientsRepository = ClientsRepository(session=db_session)
    user: Client = await repo.create(
        schema=ClientCreate(title=random_lower_string(), content=random_lower_string())
    )
    return ClientRead.from_orm(user)
