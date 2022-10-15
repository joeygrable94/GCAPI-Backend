from typing import Optional, Protocol, Tuple

from passlib.context import CryptContext

from app.api.exceptions import InvalidPasswordException
from app.core.config import settings


class PasswordHelperProtocol(Protocol):
    def verify_and_update(
        self, plain_password: str, hashed_password: str
    ) -> Tuple[bool, Optional[str]]:
        ...  # pragma: no cover

    def hash(self, password: str) -> str:
        ...  # pragma: no cover


class PasswordHelper(PasswordHelperProtocol):
    """generates, hashes, verifies and updates

    Args:
        PasswordHelperProtocol (protocol): password helper
    """

    def __init__(self, context: Optional[CryptContext] = None) -> None:
        """creates the password helper instance

        Args:
            context (Optional[CryptContext], optional):
                cryptography library. Defaults to None.
        """
        if context is None:
            self.context: CryptContext = CryptContext(
                schemes=["bcrypt"], deprecated="auto"
            )
        else:
            self.context = context  # pragma: no cover

    def verify_and_update(
        self, plain_password: str, hashed_password: str
    ) -> Tuple[bool, Optional[str]]:
        """verifies the plain password against a hashed on

        Args:
            plain_password (str): raw password string
            hashed_password (str): hashed password

        Returns:
            Tuple[bool, str]:
                - whether the password is valid
                - a verified and hashed password
        """
        return self.context.verify_and_update(plain_password, hashed_password)

    def hash(self, password: str) -> str:
        """hashes the plain password

        Args:
            password (str): raw password string

        Returns:
            str: hashed_password
        """
        return self.context.hash(password)

    async def validate_password(self, password: str) -> None:
        """validates the input password string

        Args:
            password (str): raw password string

        Raises:
            InvalidPasswordException: a reason why the input password
                is flagged as insecure.
        """
        pw_min: int = settings.PASSWORD_LENGTH_MIN
        pw_max: int = settings.PASSWORD_LENGTH_MAX
        if not len(password) >= pw_min:
            raise InvalidPasswordException(
                reason=f"Password must contain {pw_min} or more characters"
            )
        if not len(password) <= pw_max:
            raise InvalidPasswordException(
                reason=f"Password must contain {pw_max} or less characters"
            )
        return  # pragma: no cover
