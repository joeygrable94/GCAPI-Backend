from typing import Any, List
from fastapi import APIRouter, status, Request, HTTPException, Depends, Response

from app.api.errors import ErrorCode, ErrorModel
from app.api.exceptions import (UserAlreadyExists,
                                InvalidPasswordException,
                                UserNotExists,
                                InvalidID)
from app.api.openapi import OpenAPIResponseType
from app.core.security import (get_current_active_superuser,
                               get_current_active_user,
                               get_user_manager)
from app.core.security.manager import UserManager
from app.db.schemas.user import ID, U, UP, UserRead, UserUpdate


auth_users_router = APIRouter()

async def get_user_or_404(
    id: Any,
    user_manager: UserManager[UP, ID] = Depends(get_user_manager),
) -> UP:
    try:
        parsed_id = user_manager.parse_id(id)
        return await user_manager.get(parsed_id)
    except (UserNotExists, InvalidID) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e

get_user_or_404_responses: OpenAPIResponseType = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    },
}
@auth_users_router.get(
    "/me",
    response_model=UserRead,
    name="users:current_user",
    responses=get_user_or_404_responses,
)
async def me(
    user: UP = Depends(get_current_active_user),
) -> Any:
    return UserRead.from_orm(user)

update_user_me_responses: OpenAPIResponseType = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    },
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                        "summary": "A user with this email already exists.",
                        "value": {
                            "detail": ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS
                        },
                    },
                    ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                        "summary": "Password validation failed.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                                "reason": "Password should be"
                                "at least 3 characters",
                            }
                        },
                    },
                }
            }
        },
    },
}
@auth_users_router.patch(
    "/me",
    response_model=UserRead,
    dependencies=[Depends(get_current_active_user)],
    name="users:patch_current_user",
    responses=update_user_me_responses,
)
async def update_me(
    request: Request,
    user_update: UserUpdate,
    user: UP = Depends(get_current_active_user),
    user_manager: UserManager[UP, ID] = Depends(get_user_manager),
) -> Any:
    try:
        user = await user_manager.update(
            user_update, user, safe=True, request=request
        )
        return UserRead.from_orm(user)
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except UserAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
        )

get_all_users_responses: OpenAPIResponseType = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "Not a superuser.",
    },
}
@auth_users_router.get(
    "/",
    response_model=List[UserRead],
    dependencies=[Depends(get_current_active_superuser)],
    name="users:list_users",
    responses=get_all_users_responses,
)
async def get_users_list(
    request: Request,
    page: int = 1,
    user_manager: UserManager[UP, ID] = Depends(get_user_manager),
) -> Any:
    users: List = await user_manager.get_page(page=page, request=request)
    return users

get_user_reponses: OpenAPIResponseType = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "Not a superuser.",
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "The user does not exist.",
    },
}
@auth_users_router.get(
    "/{id}",
    response_model=UserRead,
    dependencies=[Depends(get_current_active_superuser)],
    name="users:user",
    responses=get_user_reponses,
)
async def get_user(user: Any = Depends(get_user_or_404)) -> Any:
    return UserRead.from_orm(user)

update_user_responses: OpenAPIResponseType = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "Not a superuser.",
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "The user does not exist.",
    },
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                        "summary": "A user with this email already exists.",
                        "value": {
                            "detail": ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS
                        },
                    },
                    ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                        "summary": "Password validation failed.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                                "reason": "Password should be"
                                "at least 3 characters",
                            }
                        },
                    },
                }
            }
        },
    },
}
@auth_users_router.patch(
    "/{id}",
    response_model=UserRead,
    dependencies=[Depends(get_current_active_superuser)],
    name="users:patch_user",
    responses=update_user_responses,
)
async def update_user(
    user_update: UserUpdate,  # type: ignore
    request: Request,
    user: UP = Depends(get_user_or_404),
    user_manager: UserManager[UP, ID] = Depends(get_user_manager),
) -> Any:
    try:
        user = await user_manager.update(
            user_update, user, safe=False, request=request
        )
        return UserRead.from_orm(user)
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except UserAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
        )

delete_user_responses: OpenAPIResponseType = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "Not a superuser.",
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "The user does not exist.",
    },
}
@auth_users_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    dependencies=[Depends(get_current_active_superuser)],
    name="users:delete_user",
    responses=delete_user_responses,
)
async def delete_user(
    user: Any = Depends(get_user_or_404),
    user_manager: UserManager[UP, ID] = Depends(get_user_manager),
) -> Any:
    await user_manager.delete(user)
    return None
