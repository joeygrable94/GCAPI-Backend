import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_email, random_lower_string

from app.db.repositories import UsersClientsRepository
from app.db.repositories.client import ClientsRepository
from app.db.repositories.user import UsersRepository
from app.db.schemas.client import ClientCreate
from app.db.schemas.user import UserCreate
from app.db.schemas.user_client import UserClientCreate
from app.db.tables import UserClient
from app.db.tables.client import Client
from app.db.tables.user import User

pytestmark = pytest.mark.asyncio


async def test_users_clients_repo_table(db_session: AsyncSession) -> None:
    repo: UsersClientsRepository = UsersClientsRepository(session=db_session)
    assert repo._table is UserClient


async def test_create_user_client_exists_by_two_none(db_session: AsyncSession) -> None:
    # create user
    user_repo: UsersRepository = UsersRepository(session=db_session)
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(email=username, password=password, is_active=True)
    user: User = await user_repo.create(schema=user_in)
    # create client
    client_repo: ClientsRepository = ClientsRepository(session=db_session)
    title: str = random_lower_string()
    content: str = random_lower_string() * 5
    client_in: ClientCreate = ClientCreate(title=title, content=content)
    client: Client = await client_repo.create(schema=client_in)
    # check user client not exists
    user_client_repo: UsersClientsRepository = UsersClientsRepository(
        session=db_session
    )
    user_client_exists: UserClient | None = await user_client_repo.exists_by_two(
        field_name_a="user_id",
        field_value_a=user.id,
        field_name_b="client_id",
        field_value_b=client.id,
    )
    assert user_client_exists is None


async def test_create_user_client_exists_by_two_found(db_session: AsyncSession) -> None:
    # create user
    user_repo: UsersRepository = UsersRepository(session=db_session)
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(email=username, password=password, is_active=True)
    user: User = await user_repo.create(schema=user_in)
    # create client
    client_repo: ClientsRepository = ClientsRepository(session=db_session)
    title: str = random_lower_string()
    content: str = random_lower_string() * 5
    client_in: ClientCreate = ClientCreate(title=title, content=content)
    client: Client = await client_repo.create(schema=client_in)
    # create user client
    user_client_repo: UsersClientsRepository = UsersClientsRepository(
        session=db_session
    )
    user_client_id: UserClientCreate = UserClientCreate(
        user_id=user.id, client_id=client.id
    )
    user_client_created: UserClient = await user_client_repo.create(user_client_id)
    # check user client not exists
    user_client_exists: UserClient | None = await user_client_repo.exists_by_two(
        field_name_a="user_id",
        field_value_a=user.id,
        field_name_b="client_id",
        field_value_b=client.id,
    )
    assert user_client_exists is user_client_created
