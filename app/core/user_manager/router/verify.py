from typing import Any, Type

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from pydantic import EmailStr

from app.core.user_manager.exceptions import (InvalidVerifyToken,
                                              UserAlreadyVerified,
                                              UserInactive, UserNotExists)
from app.core.user_manager.manager import UserManager, UserManagerDependency
from app.core.user_manager.router.common import ErrorCode, ErrorModel
from app.core.user_manager.types import ID, UP
from app.db.schemas.user import U


def get_verify_router(
    get_user_manager: UserManagerDependency[UP, ID],
    user_schema: Type[U],
) -> APIRouter:
    router = APIRouter()

    @router.post(
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

    @router.post(
        "/verify",
        response_model=user_schema,
        name="verify:verify",
        responses={
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
        },
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

    return router
