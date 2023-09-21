from fastapi import APIRouter, Depends

from app.api.deps import AsyncDatabaseSession, CurrentUser, get_async_db
from app.api.deps.permissions import get_current_user

# from app.api.openapi import users_read_responses
from app.core.auth import auth
from app.crud.user import UserRepository
from app.models.user import User
from app.schemas import UserRead
from app.schemas.user import UserCreate

router: APIRouter = APIRouter()


@router.get(
    "/me",
    name="users:current",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
    ],
    response_model=UserRead | None,
)
async def users_current(
    db: AsyncDatabaseSession,
    current_user: CurrentUser,
) -> UserRead | None:
    users_repo: UserRepository = UserRepository(session=db)
    user: User | None = await users_repo.read_by(
        field_name="auth_id", field_value=current_user.id
    )
    if not user:
        is_admin: bool = False
        if current_user.permissions and "access:admin" in current_user.permissions:
            is_admin = True
        user = await users_repo.create(
            UserCreate(
                auth_id=current_user.id,
                email=current_user.email,
                username=current_user.email,
                is_superuser=is_admin,
                is_verified=False,
                is_active=True,
            )
        )
    return UserRead.model_validate(user)


"""
@router.get(
    "/",
    name="users:list",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=List[UserReadRelations],
)
async def users_list(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetUserQueryParams,
) -> List[UserRead] | List:
    # can_access = get_current_user_authorization(current_user, "access", UserRead)
    users_repo: UserRepository = UserRepository(session=db)
    users: List[User] | List[None] | None = await users_repo.list(page=query.page)
    return [UserRead.model_validate(c) for c in users] if users else []


@router.post(
    "/",
    name="users:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=UserReadRelations,
)
async def users_create(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    user_in: UserCreate,
) -> UserRead:
    try:
        users_repo: UserRepository = UserRepository(session=db)
        data: Dict = user_in.model_dump()
        check_title: str | None = data.get("title")
        if check_title:
            a_user: User | None = await users_repo.read_by(
                field_name="title",
                field_value=check_title,
            )
            if a_user:
                raise UserAlreadyExists()
        new_user: User = await users_repo.create(user_in)
        return UserRead.model_validate(new_user)
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.CLIENT_EXISTS
        )


@router.get(
    "/{user_id}",
    name="users:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_user_or_404),
    ],
    # responses=users_read_responses,
    response_model=UserReadRelations,
)
async def users_read(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    user: FetchUserOr404,
) -> UserRead:
    return UserRead.model_validate(user)


@router.patch(
    "/{user_id}",
    name="users:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_user_or_404),
    ],
    response_model=UserReadRelations,
)
async def users_update(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    user: FetchUserOr404,
    user_in: UserUpdate,
) -> UserRead:
    try:
        users_repo: UserRepository = UserRepository(session=db)
        if user_in.title is not None:
            a_user: User | None = await users_repo.read_by(
                field_name="title", field_value=user_in.title
            )
            if a_user:
                raise UserAlreadyExists()
        updated_user: User | None = await users_repo.update(
            entry=user, schema=user_in
        )
        return (
            UserRead.model_validate(updated_user)
            if updated_user
            else UserRead.model_validate(user)
        )
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.CLIENT_EXISTS
        )


@router.delete(
    "/{user_id}",
    name="users:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_user_or_404),
    ],
    response_model=None,
)
async def users_delete(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    user: FetchUserOr404,
) -> None:
    users_repo: UserRepository = UserRepository(session=db)
    await users_repo.delete(entry=user)
    return None
"""
