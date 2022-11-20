from datetime import datetime, timedelta, timezone
from time import sleep
from typing import Any, Optional
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.utilities import get_uuid, get_uuid_str
from app.db.repositories import AccessTokensRepository
from app.db.schemas import AccessTokenCreate, AccessTokenRead, AccessTokenUpdate
from app.db.tables import AccessToken
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.anyio


async def test_token_repo_schema_read(db_session: AsyncSession) -> None:
    token_repo: AccessTokensRepository = AccessTokensRepository(session=db_session)
    assert token_repo._schema_read is AccessTokenRead


async def test_token_repo_table(db_session: AsyncSession) -> None:
    token_repo: AccessTokensRepository = AccessTokensRepository(session=db_session)
    assert token_repo._table is AccessToken


async def test_create_token(db_session: AsyncSession) -> None:
    token_repo: AccessTokensRepository = AccessTokensRepository(session=db_session)
    fake_token: str = random_lower_string()
    fake_csrf: str = get_uuid_str()
    fake_expire: datetime = datetime.now(timezone.utc) + timedelta(
        seconds=settings.ACCESS_TOKEN_LIFETIME
    )
    fake_user: UUID = get_uuid()
    token_in: AccessTokenCreate = AccessTokenCreate(
        token_jti=fake_token,
        csrf=fake_csrf,
        expires_at=fake_expire,
        user_id=fake_user,
    )
    token: AccessToken = await token_repo.create(schema=token_in)
    assert token.token_jti == fake_token
    assert token.user_id == fake_user
    assert not token.is_revoked


async def test_read_token_not_found(db_session: AsyncSession) -> None:
    token_repo: AccessTokensRepository = AccessTokensRepository(session=db_session)
    fake_token: str = random_lower_string()
    fake_csrf: str = get_uuid_str()
    fake_expire: datetime = datetime.now(timezone.utc) + timedelta(
        seconds=settings.ACCESS_TOKEN_LIFETIME
    )
    fake_user: UUID = get_uuid()
    token_in: AccessTokenCreate = AccessTokenCreate(
        token_jti=fake_token,
        csrf=fake_csrf,
        expires_at=fake_expire,
        user_id=fake_user,
    )
    token: AccessToken = await token_repo.create(schema=token_in)
    assert token.token_jti == fake_token
    assert token.user_id == fake_user
    assert not token.is_revoked
    fake_id: UUID = get_uuid()
    found_token: Optional[AccessToken] = await token_repo.read(entry_id=fake_id)
    assert not found_token


async def test_read_by_token(db_session: AsyncSession) -> None:
    token_repo: AccessTokensRepository = AccessTokensRepository(session=db_session)
    fake_user: UUID = get_uuid()
    fake_token: str = random_lower_string()
    fake_csrf: str = get_uuid_str()
    fake_expire: datetime = datetime.now(timezone.utc) + timedelta(
        seconds=settings.ACCESS_TOKEN_LIFETIME
    )
    token_in: AccessTokenCreate = AccessTokenCreate(
        token_jti=fake_token,
        csrf=fake_csrf,
        expires_at=fake_expire,
        user_id=fake_user,
    )
    token: AccessToken = await token_repo.create(schema=token_in)
    assert token.token_jti == fake_token
    assert token.user_id == fake_user
    assert not token.is_revoked
    found_token: Optional[AccessToken] = await token_repo.read_by_token(
        token_jti=fake_token, max_age=None
    )
    assert found_token
    assert token.token_jti == found_token.token_jti


async def test_read_by_token_max_age(db_session: AsyncSession) -> None:
    token_repo: AccessTokensRepository = AccessTokensRepository(session=db_session)
    fake_user: UUID = get_uuid()
    fake_token: str = random_lower_string()
    fake_csrf: str = get_uuid_str()
    fake_expire: datetime = datetime.now(timezone.utc) + timedelta(
        seconds=settings.ACCESS_TOKEN_LIFETIME
    )
    created_at = datetime.utcnow()
    sleep(1)
    token_in: AccessTokenCreate = AccessTokenCreate(
        token_jti=fake_token,
        csrf=fake_csrf,
        expires_at=fake_expire,
        user_id=fake_user,
    )
    token: AccessToken = await token_repo.create(schema=token_in)
    assert token.token_jti == fake_token
    assert token.user_id == fake_user
    assert not token.is_revoked
    found_token: Optional[AccessToken] = await token_repo.read_by_token(
        token_jti=fake_token, max_age=created_at
    )
    assert found_token
    assert token.token_jti == found_token.token_jti


async def test_read_by_token_user(db_session: AsyncSession) -> None:
    token_repo: AccessTokensRepository = AccessTokensRepository(session=db_session)
    fake_user: UUID = get_uuid()
    fake_token: str = random_lower_string()
    fake_csrf: str = get_uuid_str()
    fake_expire: datetime = datetime.now(timezone.utc) + timedelta(
        seconds=settings.ACCESS_TOKEN_LIFETIME
    )
    token_in: AccessTokenCreate = AccessTokenCreate(
        token_jti=fake_token, csrf=fake_csrf, expires_at=fake_expire, user_id=fake_user
    )
    token: AccessToken = await token_repo.create(schema=token_in)
    assert token.token_jti == fake_token
    assert token.user_id == fake_user
    assert not token.is_revoked
    found_token: Optional[AccessToken] = await token_repo.read_by(
        field_name="user_id", field_value=fake_user
    )
    assert found_token
    assert token.token_jti == found_token.token_jti
    assert found_token.user_id == fake_user


async def test_read_by_token_user_not_found(db_session: AsyncSession) -> None:
    token_repo: AccessTokensRepository = AccessTokensRepository(session=db_session)
    fake_user_2: UUID = get_uuid()
    fake_user: UUID = get_uuid()
    fake_token: str = random_lower_string()
    fake_csrf: str = get_uuid_str()
    fake_expire: datetime = datetime.now(timezone.utc) + timedelta(
        seconds=settings.ACCESS_TOKEN_LIFETIME
    )
    token_in: AccessTokenCreate = AccessTokenCreate(
        token_jti=fake_token, csrf=fake_csrf, expires_at=fake_expire, user_id=fake_user
    )
    token: AccessToken = await token_repo.create(schema=token_in)
    assert token.token_jti == fake_token
    assert token.user_id == fake_user
    assert not token.is_revoked
    found_token: Optional[AccessToken] = await token_repo.read_by(
        field_name="user_id", field_value=fake_user_2
    )
    assert not found_token


async def test_update_token(db_session: AsyncSession) -> None:
    token_repo: AccessTokensRepository = AccessTokensRepository(session=db_session)
    fake_user: UUID = get_uuid()
    fake_token: str = random_lower_string()
    fake_csrf: str = get_uuid_str()
    fake_expire: datetime = datetime.now(timezone.utc) + timedelta(
        seconds=settings.ACCESS_TOKEN_LIFETIME
    )
    token_in: AccessTokenCreate = AccessTokenCreate(
        token_jti=fake_token, csrf=fake_csrf, expires_at=fake_expire, user_id=fake_user
    )
    token: AccessToken = await token_repo.create(schema=token_in)
    assert token.token_jti == fake_token
    assert token.user_id == fake_user
    assert not token.is_revoked
    update_tok: AccessTokenUpdate = AccessTokenUpdate(is_revoked=True)
    token_2: Optional[AccessToken] = await token_repo.update(
        entry=token, schema=update_tok
    )
    assert token_2
    assert token.id == token_2.id
    assert token_2.token_jti == fake_token
    assert token_2.is_revoked


async def test_list_tokens(db_session: AsyncSession) -> None:
    token_repo: AccessTokensRepository = AccessTokensRepository(session=db_session)
    fake_user: UUID = get_uuid()
    t1: str = random_lower_string()
    fake_csrf: str = get_uuid_str()
    fake_expire: datetime = datetime.now(timezone.utc) + timedelta(
        seconds=settings.ACCESS_TOKEN_LIFETIME
    )
    t1_in: AccessTokenCreate = AccessTokenCreate(
        token_jti=t1, csrf=fake_csrf, expires_at=fake_expire, user_id=fake_user
    )
    token1: AccessToken = await token_repo.create(schema=t1_in)
    assert token1
    t2: str = random_lower_string()
    t2_in: AccessTokenCreate = AccessTokenCreate(
        token_jti=t2, csrf=fake_csrf, expires_at=fake_expire, user_id=fake_user
    )
    token2: AccessToken = await token_repo.create(schema=t2_in)
    assert token2
    tokens: Any = await token_repo.list(page=1)
    assert type(tokens) is list
