from typing import Any, Generic, Sequence, Type

from fastapi import APIRouter

from app.core.user_manager.authentication import (AuthenticationBackend,
                                                  Authenticator)
from app.core.user_manager.manager import UserManagerDependency
from app.core.user_manager.router import (get_auth_router, get_register_router,
                                          get_reset_password_router,
                                          get_users_router, get_verify_router)
from app.core.user_manager.types import ID, UP
from app.db.schemas.user import UC, UU, U


class FastAPIUsers(Generic[UP, ID]):
    """
    Main object that ties together the component for users authentication.

    :param get_user_manager: Dependency callable getter to inject the
    user manager class instance.
    :param auth_backends: List of authentication backends.

    :attribute current_user: Dependency callable getter to inject authenticated user
    with a specific set of parameters.
    """

    authenticator: Authenticator

    def __init__(
        self,
        get_user_manager: UserManagerDependency[UP, ID],
        auth_backends: Sequence[AuthenticationBackend],
    ):
        self.authenticator = Authenticator(auth_backends, get_user_manager)
        self.get_user_manager: Any = get_user_manager
        self.current_user: Any = self.authenticator.current_user

    def get_register_router(
        self, user_schema: Type[U], user_create_schema: Type[UC]
    ) -> APIRouter:
        """
        Return a router with a register route.

        :param user_schema: Pydantic schema of a public user.
        :param user_create_schema: Pydantic schema for creating a user.
        """
        return get_register_router(
            self.get_user_manager, user_schema, user_create_schema
        )

    def get_verify_router(self, user_schema: Type[U]) -> APIRouter:
        """
        Return a router with e-mail verification routes.

        :param user_schema: Pydantic schema of a public user.
        """
        return get_verify_router(self.get_user_manager, user_schema)

    def get_reset_password_router(self) -> APIRouter:
        """Return a reset password process router."""
        return get_reset_password_router(self.get_user_manager)

    def get_auth_router(
        self, backend: AuthenticationBackend, requires_verification: bool = False
    ) -> APIRouter:
        """
        Return an auth router for a given authentication backend.

        :param backend: The authentication backend instance.
        :param requires_verification: Whether the authentication
        require the user to be verified or not.
        """
        return get_auth_router(
            backend,
            self.get_user_manager,
            self.authenticator,
            requires_verification,
        )

    def get_users_router(
        self,
        user_schema: Type[U],
        user_update_schema: Type[UU],
        requires_verification: bool = False,
    ) -> APIRouter:
        """
        Return a router with routes to manage users.

        :param user_schema: Pydantic schema of a public user.
        :param user_update_schema: Pydantic schema for updating a user.
        :param requires_verification: Whether the endpoints
        require the users to be verified or not.
        """
        return get_users_router(
            self.get_user_manager,
            user_schema,
            user_update_schema,
            self.authenticator,
            requires_verification,
        )
