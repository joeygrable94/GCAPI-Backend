import datetime
import json
from typing import Any

from sqlalchemy import VARCHAR, Dialect, Text
from sqlalchemy.types import TypeDecorator, TypeEngine
from sqlalchemy_utils.exceptions import ImproperlyConfigured  # type: ignore
from sqlalchemy_utils.types.encrypted.encrypted_type import (  # type: ignore  # noqa: E501
    DatetimeHandler,
)
from sqlalchemy_utils.types.json import JSONType  # type: ignore
from sqlalchemy_utils.types.scalar_coercible import ScalarCoercible  # type: ignore

from app.core.config import settings
from app.core.security.encryption.cipher_secure import SecureMessage
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_STORED

crypto = None
try:
    import cryptography  # noqa: F401

    crypto = True
except ImportError:  # pragma: no cover
    crypto = False


class EncryptedString(TypeDecorator, ScalarCoercible):
    """

    Example:

        class User(Base):
            __tablename__ = "user"
            id = Column(Integer, primary_key=True)
            access_token: str = Column(
                EncryptedString(
                    String,
                    255
                )
            )
            unicode_data: str = Column(
                EncryptedString(
                    Unicode,
                    1000
                )
            )
            is_active: bool = Column(
                EncryptedString(
                    Boolean,
                )
            )
            is_optional: bool | None = Column(
                EncryptedString(
                    Boolean,
                    nullable=True
                )
            )

    """

    impl = Text
    cache_ok = True

    def __init__(
        self,
        type_in: Any,
        length: int | None = None,
        nullable: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialization."""
        if not crypto:
            raise ImproperlyConfigured(
                "'cryptography' is required to use EncryptedString."
            )
        super().__init__(**kwargs)
        # set the underlying type
        if isinstance(type_in, type):
            if length is None:
                if callable(type_in):
                    type_in = type_in()
                else:
                    type_in = type_in
            else:
                if callable(type_in):
                    type_in = type_in(length=length)
                else:
                    type_in = type_in
        self.length = length
        self.underlying_type = type_in
        self.nullable = nullable
        self.engine = SecureMessage(
            pass_key=settings.api.encryption_key,
            salt=settings.api.encryption_salt,
        )

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, value: str) -> None:
        self._key = value

    def load_dialect_impl(
        self, dialect: Dialect
    ) -> TypeEngine[str]:  # pragma: no cover
        if dialect.name == "mysql":
            if self.length:
                return dialect.type_descriptor(VARCHAR(length=self.length))
            else:
                return dialect.type_descriptor(Text(DB_STR_TINYTEXT_MAXLEN_STORED))
        else:
            return dialect.type_descriptor(Text(length=self.length))

    def process_bind_param(self, value: Any, dialect: Dialect) -> Any:
        """Encrypt a value on the way in."""
        if value is not None:
            try:
                value = self.underlying_type.process_bind_param(value, dialect)
            except AttributeError:
                # Doesn't have 'process_bind_param'
                # Handle 'boolean' and 'dates'
                type_ = self.underlying_type.python_type
                if issubclass(type_, bool):
                    value = True if value else False
                elif issubclass(
                    type_, (datetime.datetime, datetime.date, datetime.time)
                ):
                    value = value.isoformat()
                elif issubclass(type_, JSONType):
                    value = json.dumps(value)
            stored_value = self.engine.sign_and_encrypt(value)
            return stored_value
        if self.nullable:
            return None

    def process_result_value(self, value: Any, dialect: Dialect) -> Any:
        """Decrypt value on the way out."""
        if value is not None:
            decrypted_value = self.engine.decrypt_and_verify(
                value, self.underlying_type.python_type
            )
            try:
                return self.underlying_type.process_result_value(
                    decrypted_value, dialect
                )
            except AttributeError:
                # Doesn't have 'process_result_value'
                # Handle 'boolean' and 'dates'
                type_ = self.underlying_type.python_type
                date_types = [datetime.datetime, datetime.time, datetime.date]
                if issubclass(type_, bool):
                    return decrypted_value is True
                elif type_ in date_types:
                    return DatetimeHandler.process_value(decrypted_value, type_)
                elif issubclass(type_, JSONType):
                    return json.loads(str(decrypted_value))
                # Handle all others
                return self.underlying_type.python_type(decrypted_value)
        if self.nullable:
            return None

    def _coerce(self, value: Any) -> Any:
        if isinstance(self.underlying_type, ScalarCoercible):
            return self.underlying_type._coerce(value)
        return value
