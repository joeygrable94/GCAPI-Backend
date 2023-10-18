from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_email

from app.core.security import Auth0User, UserRole
from app.crud import UserRepository
from app.models import User
from app.schemas import UserCreate, UserRead


async def create_user_from_auth0(
    db_session: AsyncSession, current_user: Auth0User
) -> UserRead:
    users_repo: UserRepository = UserRepository(session=db_session)
    user: User | None = await users_repo.read_by(
        field_name="auth_id", field_value=current_user.auth_id
    )
    if not user:
        user_roles: List[UserRole] = []
        if current_user.permissions:
            for user_perm in current_user.permissions:
                user_roles.append(UserRole[user_perm])
        user = await users_repo.create(
            UserCreate(
                auth_id=current_user.auth_id,
                email=random_email() if not current_user.email else current_user.email,
                username=random_email()
                if not current_user.email
                else current_user.email,
                is_superuser=False,
                is_verified=False,
                is_active=True,
                roles=user_roles,
            )
        )
    return UserRead.model_validate(user)
