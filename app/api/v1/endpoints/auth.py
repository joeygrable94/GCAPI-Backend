from typing import Any, Tuple
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.errors import ErrorModel, ErrorCode
from app.api.openapi import OpenAPIResponseType
from app.core.config import settings
from app.core.security import auth_backend, get_user_manager, get_current_user_token
from app.core.security.authentication.strategy.base import Strategy
from app.core.security.manager import UserManager
from app.db.schemas.user import ID, UP


auth_router: APIRouter = APIRouter()

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
@auth_router.post(
    "/login",
    name=f"auth:{auth_backend.name}.login",
    responses=login_responses,
)
async def login(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_manager: UserManager[UP, ID] = Depends(get_user_manager),
    strategy: Strategy[UP, ID] = Depends(auth_backend.get_strategy),
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
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        }
    },
    **auth_backend.transport.get_openapi_logout_responses_success(),
}
@auth_router.post(
    "/logout",
    name=f"auth:{auth_backend.name}.logout",
    responses=logout_responses
)
async def logout(
    response: Response,
    user_token: Tuple[UP, str] = Depends(get_current_user_token),
    strategy: Strategy[UP, ID] = Depends(auth_backend.get_strategy),
) -> Any:
    user, token = user_token
    return await auth_backend.logout(strategy, user, token, response)
