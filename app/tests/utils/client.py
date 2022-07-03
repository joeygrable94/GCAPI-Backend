from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.client import ClientsRepository
from app.db.schemas import ClientCreate, ClientRead
from app.tests.utils.utils import random_lower_string


async def create_random_client(db_session: AsyncSession) -> ClientRead:
    title: str = random_lower_string()
    content: str = random_lower_string()
    clients_repo: ClientsRepository = ClientsRepository(session=db_session)
    client: ClientRead = await clients_repo.create(
        ClientCreate(title=title, content=content)
    )
    return client
