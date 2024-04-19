"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseRepository
from app.models import BdxFeed

pytestmark = pytest.mark.asyncio


async def test_example(db_session: AsyncSession) -> None:
    repo: BaseRepository = BaseRepository(session=db_session)
    assert repo._table is BdxFeed

"""
