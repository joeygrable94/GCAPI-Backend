from typing import Type

from app.crud.base import BaseRepository
from app.models import Note
from app.schemas import NoteCreate, NoteRead, NoteUpdate


class NoteRepository(BaseRepository[NoteCreate, NoteRead, NoteUpdate, Note]):
    @property
    def _table(self) -> Type[Note]:  # type: ignore
        return Note
