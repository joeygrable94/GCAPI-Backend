from typing import Optional

from fastapi import APIRouter, Depends, status

from app.db.schemas import UserRead
from app.security import get_current_active_user

router = APIRouter()


@router.get(
    "/me",
    name="users:current_user",
    dependencies=[Depends(get_current_active_user)],
    # responses=get_user_or_404_responses,
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def me(
    current_user: UserRead = Depends(get_current_active_user),
) -> Optional[UserRead]:
    """
    Allows current-active-verified-users to fetch the details on their account.
    """
    return current_user
