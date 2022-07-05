from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from pydantic import EmailStr

from app.api.errors import ErrorCode, ErrorModel
from app.api.exceptions import (
    UserNotExists,
    UserInactive,
    InvalidPasswordException,
    InvalidResetPasswordToken,
)
from app.core.security import get_user_manager
from app.core.security.manager import UserManager
from app.api.openapi import OpenAPIResponseType
from app.db.schemas.user import ID, UP


reset_password_router = APIRouter()

@reset_password_router.post(
    "/forgot-password",
    status_code=status.HTTP_202_ACCEPTED,
    name="reset:forgot_password",
)
async def forgot_password(
    request: Request,
    email: EmailStr = Body(..., embed=True),
    user_manager: UserManager[UP, ID] = Depends(get_user_manager),
) -> Any:
    try:
        user = await user_manager.get_by_email(email)
    except UserNotExists:
        return None

    try:
        await user_manager.forgot_password(user, request)
    except UserInactive:
        pass

    return None

reset_password_responses: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.RESET_PASSWORD_BAD_TOKEN: {
                        "summary": "Bad or expired token.",
                        "value": {"detail": ErrorCode.RESET_PASSWORD_BAD_TOKEN},
                    },
                    ErrorCode.RESET_PASSWORD_INVALID_PASSWORD: {
                        "summary": "Password validation failed.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
                                "reason": "Password should be at least 3 characters",
                            }
                        },
                    },
                }
            }
        },
    },
}
@reset_password_router.post(
    "/reset-password",
    name="reset:reset_password",
    responses=reset_password_responses,
)
async def reset_password(
    request: Request,
    token: str = Body(...),
    password: str = Body(...),
    user_manager: UserManager[UP, ID] = Depends(get_user_manager),
) -> Any:
    try:
        await user_manager.reset_password(token, password, request)
    except (
        InvalidResetPasswordToken,
        UserNotExists,
        UserInactive,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
        )
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
