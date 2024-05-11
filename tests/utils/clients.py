from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string

from app.crud import (
    ClientRepository,
    ClientWebsiteRepository,
    DataBucketRepository,
    UserClientRepository,
)
from app.models import Client, ClientWebsite, DataBucket, User, UserClient, Website
from app.schemas import (
    ClientCreate,
    ClientRead,
    ClientWebsiteCreate,
    DataBucketCreate,
    DataBucketRead,
    UserClientCreate,
    UserRead,
    WebsiteRead,
)


async def create_random_client(db_session: AsyncSession) -> ClientRead:
    repo: ClientRepository = ClientRepository(session=db_session)
    client: Client = await repo.create(
        schema=ClientCreate(
            title=random_lower_string(), description=random_lower_string()
        )
    )
    return ClientRead.model_validate(client)


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


async def create_random_data_bucket(
    db_session: AsyncSession,
    client_id: UUID4,
) -> DataBucketRead:
    repo: DataBucketRepository = DataBucketRepository(session=db_session)
    data_bucket: DataBucket = await repo.create(
        schema=DataBucketCreate(
            bucket_name=random_lower_string(),
            bucket_prefix=random_lower_string(),
            description=random_lower_string(),
            client_id=client_id,
        )
    )
    return DataBucketRead.model_validate(data_bucket)
