from typing import Any
from fastapi import APIRouter, status, Request, HTTPException, Depends, Body
from pydantic import EmailStr

from app.api.errors import ErrorCode, ErrorModel
from app.api.exceptions import (UserNotExists,
                                UserInactive,
                                UserAlreadyVerified,
                                InvalidVerifyToken)
from app.api.openapi import OpenAPIResponseType
from app.core.security import get_user_manager
from app.core.security.manager import UserManager
from app.db.schemas.user import ID, UP, UserRead


verify_router = APIRouter()

verify_token_responses: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.VERIFY_USER_BAD_TOKEN: {
                        "summary": "Bad token, not existing user or"
                        "not the e-mail currently set for the user.",
                        "value": {"detail": ErrorCode.VERIFY_USER_BAD_TOKEN},
                    },
                    ErrorCode.VERIFY_USER_ALREADY_VERIFIED: {
                        "summary": "The user is already verified.",
                        "value": {
                            "detail": ErrorCode.VERIFY_USER_ALREADY_VERIFIED
                        },
                    },
                }
            }
        },
    }
}
@verify_router.post(
    "/request-verify-token",
    status_code=status.HTTP_202_ACCEPTED,
    name="verify:request-token",
)
async def request_verify_token(
    request: Request,
    email: EmailStr = Body(..., embed=True),
    user_manager: UserManager[UP, ID] = Depends(get_user_manager),
) -> Any:
    try:
        user = await user_manager.get_by_email(email)
        await user_manager.request_verify(user, request)
    except (
        UserNotExists,
        UserInactive,
        UserAlreadyVerified,
    ):
        pass

    return None

@verify_router.post(
    "/verify",
    response_model=UserRead,
    name="verify:verify",
    responses=verify_token_responses,
)
async def verify(
    request: Request,
    token: str = Body(..., embed=True),
    user_manager: UserManager[UP, ID] = Depends(get_user_manager),
) -> Any:
    try:
        return await user_manager.verify(token, request)
    except (InvalidVerifyToken, UserNotExists):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
        )
    except UserAlreadyVerified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.VERIFY_USER_ALREADY_VERIFIED,
        )
