from typing import Any, Dict, Generic, Optional, Type

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user_manager.types import ID, UP
from app.db.repositories.base import sql_select


class SQLAlchemyUserDatabase(Generic[UP, ID]):
    """
    Database adapter for SQLAlchemy.

    :param session: SQLAlchemy session instance.
    :param user_table: SQLAlchemy user model.
    """

    session: AsyncSession
    user_table: Type[UP]

    def __init__(
        self,
        session: AsyncSession,
        user_table: Type[UP],
    ):
        self.session: Any = session
        self.user_table: Any = user_table

    async def _get_user(self, statement: Any) -> Optional[UP]:
        results: Any = await self.session.execute(statement)
        user: Any = results.first()
        if user is None:
            return None
        return user[0]

    async def get(self, id: ID) -> Optional[UP]:
        statement: Any = sql_select(self.user_table).where(  # type: ignore
            self.user_table.id == id
        )
        return await self._get_user(statement)

    async def get_by_email(self, email: str) -> Optional[UP]:
        statement: Any = sql_select(self.user_table).where(  # type: ignore
            func.lower(self.user_table.email) == func.lower(email)
        )
        return await self._get_user(statement)

    async def create(self, create_dict: Dict[str, Any]) -> UP:
        user: Any = self.user_table(**create_dict)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user: UP, update_dict: Dict[str, Any]) -> UP:
        for key, value in update_dict.items():
            setattr(user, key, value)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user: UP) -> None:
        await self.session.delete(user)
        await self.session.commit()
