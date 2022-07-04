from typing import Optional, Protocol, Tuple

from passlib import pwd  # type: ignore
from passlib.context import CryptContext  # type: ignore


class PasswordHelperProtocol(Protocol):
    def verify_and_update(
        self, plain_password: str, hashed_password: str
    ) -> Tuple[bool, str]:
        ...  # pragma: no cover

    def hash(self, password: str) -> str:
        ...  # pragma: no cover

    def generate(self) -> str:
        ...  # pragma: no cover


class PasswordHelper(PasswordHelperProtocol):
    def __init__(self, context: Optional[CryptContext] = None) -> None:
        if context is None:
            self.context: CryptContext = CryptContext(
                schemes=["bcrypt"], deprecated="auto"
            )
        else:
            self.context = context  # pragma: no cover

    def verify_and_update(
        self, plain_password: str, hashed_password: str
    ) -> Tuple[bool, str]:
        return self.context.verify_and_update(plain_password, hashed_password)

    def hash(self, password: str) -> str:
        return self.context.hash(password)

    def generate(self) -> str:
        return pwd.genword()
