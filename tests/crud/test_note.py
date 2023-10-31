import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import NoteRepository
from app.models import Note

pytestmark = pytest.mark.asyncio


async def test_note_repo_table(db_session: AsyncSession) -> None:
    repo: NoteRepository = NoteRepository(session=db_session)
    assert repo._table is Note
