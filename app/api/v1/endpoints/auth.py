from typing import Any, Tuple

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.api.errors import (
    ErrorCode,
    ErrorModel
) 
from app.api.exceptions import (
    InvalidPasswordException,
    InvalidResetPasswordToken,
    InvalidVerifyToken,
    UserNotExists,
    UserAlreadyExists, 
    UserInactive,
    UserAlreadyVerified
)
from app.api import OpenAPIResponseType
from app.core.config import settings
from app.core.security import (
    auth_backend,
    get_current_user_token,
    get_user_manager
)
from app.core.security.authentication import Strategy
from app.core.security.manager import UserManager
from app.db.schemas import ID, UP, UserCreate, UserRead


router = APIRouter()


login_responses: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.LOGIN_BAD_CREDENTIALS: {
                        "summary": "Bad credentials or the user is inactive.",
                        "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
                    },
                    ErrorCode.LOGIN_USER_NOT_VERIFIED: {
                        "summary": "The user is not verified.",
                        "value": {"detail": ErrorCode.LOGIN_USER_NOT_VERIFIED},
                    },
                }
            }
        },
    },
    **auth_backend.transport.get_openapi_login_responses_success(),
}

@router.post(
    "/jwt/login",
    name=f"auth:{auth_backend.name}.login",
    responses=login_responses,
)
async def login(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_manager: UserManager[UP, ID] = Depends(get_user_manager),
    strategy: Strategy[UP, ID] = Depends(auth_backend.get_strategy),  # type: ignore
) -> Any:
    user: Any = await user_manager.authenticate(credentials)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
        )
    if settings.USERS_REQUIRE_VERIFICATION and not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
        )
    return await auth_backend.login(strategy, user, response)


logout_responses: OpenAPIResponseType = {
    **{
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
    **auth_backend.transport.get_openapi_logout_responses_success(),
}

@router.post(
    "/jwt/logout", name=f"auth:{auth_backend.name}.logout", responses=logout_responses
)
async def logout(
    response: Response,
    user_token: Tuple[UP, str] = Depends(get_current_user_token),
    strategy: Strategy[UP, ID] = Depends(auth_backend.get_strategy),  # type: ignore
) -> Any:
    user, token = user_token
    return await auth_backend.logout(strategy, user, token, response)


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

@router.post(
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
                        "value": {"detail": ErrorCode.VERIFY_USER_ALREADY_VERIFIED},
                    },
                }
            }
        },
    }
}

@router.post(
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


@router.post(
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

@router.post(
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
