from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string

from app.crud import NoteRepository
from app.models import Note
from app.schemas import NoteCreate
from app.schemas import NoteRead


async def create_random_note(db_session: AsyncSession, user_id: UUID4) -> NoteRead:
    repo: NoteRepository = NoteRepository(session=db_session)
    note: Note = await repo.create(
        schema=NoteCreate(
            title=random_lower_string(),
            description=random_lower_string(),
            user_id=user_id,
        )
    )
    return NoteRead.model_validate(note)
