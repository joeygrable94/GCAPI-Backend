from typing import List, Type
from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_, select as sql_select

from app.crud.base import BaseRepository
from app.models import Note, User
from app.schemas import NoteCreate, NoteRead, NoteUpdate


class NoteRepository(BaseRepository[NoteCreate, NoteRead, NoteUpdate, Note]):
    @property
    def _table(self) -> Type[Note]:  # type: ignore
        return Note

    def query_list(
        self,
        user_id: UUID | None = None,
    ) -> Select:
        # create statement joins
        stmt: Select = sql_select(self._table)
        # create conditions
        conditions: List[BinaryExpression[bool]] = []
        # append conditions
        if user_id:  # TODO: test
            stmt = stmt.join(User, Note.user_id == User.id)
            conditions.append(User.id.like(user_id))
        # apply conditions
        if len(conditions) > 0:  # TODO: test
            stmt = stmt.where(and_(*conditions))
        return stmt
