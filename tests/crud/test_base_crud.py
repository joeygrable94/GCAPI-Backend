import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_boolean, random_email

from app.core.utilities.uuids import get_random_username, get_uuid_str
from app.crud import ClientRepository, UserRepository
from app.db.constants import DB_STR_USER_PICTURE_DEFAULT
from app.schemas import ClientCreate, UserCreate

pytestmark = pytest.mark.asyncio


async def test_client_encrypted_in_db(db_session: AsyncSession) -> None:
    repo: ClientRepository = ClientRepository(session=db_session)
    client = await repo.create(
        schema=ClientCreate(
            title="Test Client",
            description="This is a test client",
        )
    )
    assert client.title == "Test Client"


async def test_client_encrypted_too_in_db(db_session: AsyncSession) -> None:
    repo: ClientRepository = ClientRepository(session=db_session)
    client = await repo.create(
        schema=ClientCreate(
            title="Test Client 2",
        )
    )
    assert client.title == "Test Client 2"


async def test_user_encrypted_in_db(db_session: AsyncSession) -> None:
    a_authid = get_uuid_str()
    a_email = random_email()
    a_username = get_random_username()
    a_active = random_boolean()
    a_verified = random_boolean()
    a_superuser = random_boolean()
    a_picture = DB_STR_USER_PICTURE_DEFAULT
    a_scopes = ["role:user", "role:admin"]
    repo: UserRepository = UserRepository(session=db_session)
    db_user = await repo.create(
        schema=UserCreate(
            auth_id=a_authid,
            email=a_email,
            username=a_username,
            picture=a_picture,
            is_active=a_active,
            is_verified=a_verified,
            is_superuser=a_superuser,
            scopes=a_scopes,
        )
    )
    assert db_user.auth_id == a_authid
