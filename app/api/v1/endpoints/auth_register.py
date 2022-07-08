from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.api.errors import ErrorCode, ErrorModel
from app.api.exceptions import InvalidPasswordException, UserAlreadyExists
from app.api.openapi import OpenAPIResponseType
from app.core.security import get_user_manager
from app.core.security.manager import UserManager
from app.db.schemas import ID, UP, UserCreate, UserRead

register_router: APIRouter = APIRouter()

register_responses: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                        "summary": "A user with this email already exists.",
                        "value": {"detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS},
                    },
                    ErrorCode.REGISTER_INVALID_PASSWORD: {
                        "summary": "Password validation failed.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                                "reason": "Password should be" "at least 3 characters",
                            }
                        },
                    },
                }
            }
        },
    },
}


@register_router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    name="register:register",
    responses=register_responses,
)
async def register(
    request: Request,
    user_create: UserCreate,
    user_manager: UserManager[UP, ID] = Depends(get_user_manager),
) -> Any:
    try:
        created_user = await user_manager.create(
            user_create, safe=True, request=request
        )
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )

    return UserRead.from_orm(created_user)
