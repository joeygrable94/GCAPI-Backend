import uuid
from typing import Any, Dict, Generic, List, Optional, Union

import jwt
from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from app.api.paginate import paginate

from app.core.config import settings
from app.api.exceptions import (InvalidID,
                                InvalidResetPasswordToken,
                                InvalidVerifyToken,
                                UserAlreadyExists,
                                UserAlreadyVerified,
                                UserInactive, UserNotExists)
from app.core.security.jwt import SecretType, decode_jwt, generate_jwt
from app.core.security.password import (PasswordHelper,
                                        PasswordHelperProtocol)
from app.db.user_db import SQLAlchemyUserDatabase
from app.db.schemas.user import ID, UP, UC, UU


class UserManager(Generic[UP, ID]):
    """
    User management logic.

    :attribute reset_password_token_secret: Secret to encode reset password token.
    :attribute reset_password_token_lifetime_seconds: Lifetime of reset password token.
    :attribute reset_password_token_audience: JWT audience of reset password token.
    :attribute verification_token_secret: Secret to encode verification token.
    :attribute verification_token_lifetime_seconds: Lifetime of verification token.
    :attribute verification_token_audience: JWT audience of verification token.

    :param user_db: Database adapter instance.
    """

    reset_password_token_secret: SecretType = settings.SECRET_KEY
    reset_password_token_lifetime_seconds: int = settings.ACCESS_TOKEN_LIFETIME
    reset_password_token_audience: str = settings.RESET_PASSWORD_TOKEN_AUDIENCE

    verification_token_secret: SecretType = settings.SECRET_KEY
    verification_token_lifetime_seconds: int = settings.ACCESS_TOKEN_LIFETIME
    verification_token_audience: str = settings.VERIFY_USER_TOKEN_AUDIENCE

    user_db: SQLAlchemyUserDatabase[UP, ID]
    password_helper: PasswordHelperProtocol

    def __init__(
        self,
        user_db: SQLAlchemyUserDatabase[UP, ID],
        password_helper: Optional[PasswordHelperProtocol] = None,
    ):
        self.user_db = user_db
        if password_helper is None:
            self.password_helper = PasswordHelper()
        else:
            self.password_helper = password_helper  # pragma: no cover

    def parse_id(self, value: Any) -> ID:
        """
        Parse a value into a correct ID instance.

        :param value: The value to parse.
        :raises InvalidID: The ID value is invalid.
        :return: An ID object.
        """
        if isinstance(value, uuid.UUID):
            return value  # type: ignore
        try:
            return uuid.UUID(value)  # type: ignore
        except ValueError as e:
            raise InvalidID() from e

    async def get(self, id: ID) -> UP:
        """
        Get a user by id.

        :param id: Id. of the user to retrieve.
        :raises UserNotExists: The user does not exist.
        :return: A user.
        """
        user = await self.user_db.get(id)
        if user is None:
            raise UserNotExists()
        return user

    async def get_by_email(self, user_email: str) -> UP:
        """
        Get a user by e-mail.

        :param user_email: E-mail of the user to retrieve.
        :raises UserNotExists: The user does not exist.
        :return: A user.
        """
        user = await self.user_db.get_by_email(user_email)
        if user is None:
            raise UserNotExists()
        return user

    async def get_page(
        self,
        page: int = 1,
        request: Optional[Request] = None
    ) -> List[UP]:
        skip, limit = paginate(page)
        users = await self.user_db.get_list(limit=limit, skip=skip)
        if users is None:
            return []
        return users

    async def create(
        self,
        user_create: UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def request_verify(self, user: UP, request: Optional[Request] = None) -> None:
        """
        Start a verification request.

        Triggers the on_after_request_verify handler on success.

        :param user: The user to verify.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserInactive: The user is inactive.
        :raises UserAlreadyVerified: The user is already verified.
        """
        if not user.is_active:
            raise UserInactive()
        if user.is_verified:
            raise UserAlreadyVerified()

        token_data = {
            "user_id": str(user.id),
            "email": user.email,
            "aud": self.verification_token_audience,
        }
        token = generate_jwt(
            token_data,
            self.verification_token_secret,
            self.verification_token_lifetime_seconds,
        )
        await self.on_after_request_verify(user, token, request)

    async def verify(self, token: str, request: Optional[Request] = None) -> UP:
        """
        Validate a verification request.

        Changes the is_verified flag of the user to True.

        Triggers the on_after_verify handler on success.

        :param token: The verification token generated by request_verify.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises InvalidVerifyToken: The token is invalid or expired.
        :raises UserAlreadyVerified: The user is already verified.
        :return: The verified user.
        """
        try:
            data = decode_jwt(
                token,
                self.verification_token_secret,
                [self.verification_token_audience],
            )
        except jwt.PyJWTError:
            raise InvalidVerifyToken()

        try:
            user_id = data["user_id"]
            email = data["email"]
        except KeyError:
            raise InvalidVerifyToken()

        try:
            user = await self.get_by_email(email)
        except UserNotExists:
            raise InvalidVerifyToken()

        try:
            parsed_id = self.parse_id(user_id)
        except InvalidID:
            raise InvalidVerifyToken()
        if parsed_id != user.id:
            raise InvalidVerifyToken()
        if user.is_verified:
            raise UserAlreadyVerified()
        verified_user = await self._update(user, {"is_verified": True})
        await self.on_after_verify(verified_user, request)
        return verified_user

    async def forgot_password(
        self, user: UP, request: Optional[Request] = None
    ) -> None:
        """
        Start a forgot password request.

        Triggers the on_after_forgot_password handler on success.

        :param user: The user that forgot its password.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserInactive: The user is inactive.
        """
        if not user.is_active:
            raise UserInactive()

        token_data = {
            "user_id": str(user.id),
            "aud": self.reset_password_token_audience,
        }
        token = generate_jwt(
            token_data,
            self.reset_password_token_secret,
            self.reset_password_token_lifetime_seconds,
        )
        await self.on_after_forgot_password(user, token, request)

    async def reset_password(
        self, token: str, password: str, request: Optional[Request] = None
    ) -> UP:
        """
        Reset the password of a user.

        Triggers the on_after_reset_password handler on success.

        :param token: The token generated by forgot_password.
        :param password: The new password to set.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises InvalidResetPasswordToken: The token is invalid or expired.
        :raises UserInactive: The user is inactive.
        :raises InvalidPasswordException: The password is invalid.
        :return: The user with updated password.
        """
        try:
            data = decode_jwt(
                token,
                self.reset_password_token_secret,
                [self.reset_password_token_audience],
            )
        except jwt.PyJWTError:
            raise InvalidResetPasswordToken()

        try:
            user_id = data["user_id"]
        except KeyError:
            raise InvalidResetPasswordToken()

        try:
            parsed_id = self.parse_id(user_id)
        except InvalidID:
            raise InvalidResetPasswordToken()

        user = await self.get(parsed_id)
        if not user.is_active:
            raise UserInactive()
        updated_user = await self._update(user, {"password": password})
        await self.on_after_reset_password(user, request)
        return updated_user

    async def update(
        self,
        user_update: UU,
        user: UP,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> UP:
        """
        Update a user.

        Triggers the on_after_update handler on success

        :param user_update: The UserUpdate model containing
        the changes to apply to the user.
        :param user: The current user to update.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the update, defaults to False
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :return: The updated user.
        """
        if safe:
            updated_user_data = user_update.create_update_dict()
        else:
            updated_user_data = user_update.create_update_dict_superuser()
        updated_user = await self._update(user, updated_user_data)
        await self.on_after_update(updated_user, updated_user_data, request)
        return updated_user

    async def delete(self, user: UP) -> None:
        """
        Delete a user.

        :param user: The user to delete.
        """
        await self.user_db.delete(user)

    # *You should overload this method to add your own validation logic.*
    async def validate_password(self, password: str, user: Union[UC, UP]) -> None:
        """
        Validate a password.

        :param password: The password to validate.
        :param user: The user associated to this password.
        :raises InvalidPasswordException: The password is invalid.
        :return: None if the password is valid.
        """
        return  # pragma: no cover

    # *You should overload this method to add your own logic.*
    async def on_after_register(
        self, user: UP, request: Optional[Request] = None
    ) -> None:
        """
        Perform logic after successful user registration.

        :param user: The registered user
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        """
        print(f"User {user.id} has registered.")
        return  # pragma: no cover

    # *You should overload this method to add your own logic.*
    async def on_after_update(
        self,
        user: UP,
        update_dict: Dict[str, Any],
        request: Optional[Request] = None,
    ) -> None:
        """
        Perform logic after successful user update.

        :param user: The updated user
        :param update_dict: Dictionary with the updated user fields.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        """
        return  # pragma: no cover

    # *You should overload this method to add your own logic.*
    async def on_after_request_verify(
        self, user: UP, token: str, request: Optional[Request] = None
    ) -> None:
        """
        Perform logic after successful verification request.

        :param user: The user to verify.
        :param token: The verification token.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        """
        print(f"Verification requested for user {user.id}.")
        print(f"Verification token: {token}")
        return  # pragma: no cover

    # *You should overload this method to add your own logic.*
    async def on_after_verify(
        self, user: UP, request: Optional[Request] = None
    ) -> None:
        """
        Perform logic after successful user verification.

        :param user: The verified user.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        """
        return  # pragma: no cover

    # *You should overload this method to add your own logic.*
    async def on_after_forgot_password(
        self, user: UP, token: str, request: Optional[Request] = None
    ) -> None:
        """
        Perform logic after successful forgot password request.

        :param user: The user that forgot its password.
        :param token: The forgot password token.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        """
        print(f"User {user.id} has forgot their password.")
        print(f"Reset token: {token}")
        return  # pragma: no cover

    # *You should overload this method to add your own logic.*
    async def on_after_reset_password(
        self, user: UP, request: Optional[Request] = None
    ) -> None:
        """
        Perform logic after successful password reset.

        :param user: The user that reset its password.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        """
        return  # pragma: no cover

    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[UP]:
        """
        Authenticate and return a user following an email and a password.

        Will automatically upgrade password hash if necessary.

        :param credentials: The user credentials.
        """
        try:
            user = await self.get_by_email(credentials.username)
        except UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user

    async def _update(self, user: UP, update_dict: Dict[str, Any]) -> UP:
        validated_update_dict = {}
        for field, value in update_dict.items():
            if field == "email" and value != user.email:
                try:
                    await self.get_by_email(value)
                    raise UserAlreadyExists()
                except UserNotExists:
                    validated_update_dict["email"] = value
                    validated_update_dict["is_verified"] = False
            elif field == "password":
                await self.validate_password(value, user)
                validated_update_dict["hashed_password"] = self.password_helper.hash(
                    value
                )
            else:
                validated_update_dict[field] = value
        return await self.user_db.update(user, validated_update_dict)
