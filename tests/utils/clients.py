from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string

from app.crud import ClientRepository
from app.crud.client_website import ClientWebsiteRepository
from app.crud.user_client import UserClientRepository
from app.models import Client
from app.models.client_website import ClientWebsite
from app.models.user import User
from app.models.user_client import UserClient
from app.models.website import Website
from app.schemas import ClientCreate, ClientRead
from app.schemas.client_website import ClientWebsiteCreate
from app.schemas.user import UserRead
from app.schemas.user_client import UserClientCreate
from app.schemas.website import WebsiteRead


async def create_random_client(db_session: AsyncSession) -> ClientRead:
    repo: ClientRepository = ClientRepository(session=db_session)
    user: Client = await repo.create(
        schema=ClientCreate(
            title=random_lower_string(), description=random_lower_string()
        )
    )
    return ClientRead.model_validate(user)


async def assign_user_to_client(
    db_session: AsyncSession, user: User | UserRead, client: Client | ClientRead
) -> UserClient:
    repo: UserClientRepository = UserClientRepository(session=db_session)
    user_client: UserClient = await repo.create(
        schema=UserClientCreate(user_id=user.id, client_id=client.id)
    )
    return user_client


async def assign_website_to_client(
    db_session: AsyncSession,
    website: Website | WebsiteRead,
    client: Client | ClientRead,
) -> ClientWebsite:
    repo: ClientWebsiteRepository = ClientWebsiteRepository(session=db_session)
    client_website: ClientWebsite = await repo.create(
        schema=ClientWebsiteCreate(website_id=website.id, client_id=client.id)
    )
    return client_website
