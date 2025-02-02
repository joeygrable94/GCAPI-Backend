from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from app.entities.api.dependencies import AsyncDatabaseSession
from app.entities.user.crud import User, UserRepository
from app.entities.user.errors import UserNotFound
from app.utilities import parse_id


async def get_user_or_404(
    db: AsyncDatabaseSession,
    user_id: Any,
) -> User | None:
    """Parses uuid/int and fetches user by id."""
    parsed_id: UUID = parse_id(user_id)
    user_repo: UserRepository = UserRepository(session=db)
    user: User | None = await user_repo.read(entry_id=parsed_id)
    if user is None:
        raise UserNotFound()
    return user


FetchUserOr404 = Annotated[User, Depends(get_user_or_404)]
