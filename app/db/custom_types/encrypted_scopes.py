from typing import Any, List

from sqlalchemy import BLOB, TypeDecorator
from sqlalchemy.engine.interfaces import Dialect

from app.core.config import settings
from app.core.security.encryption.cipher_secure import SecureMessage
from app.core.utilities import scope_regex
from app.db.constants import DB_STR_BLOB_MAXLEN_INPUT, DB_STR_BLOB_MAXLEN_STORED


class EncryptedScopes(TypeDecorator):
    cache_ok = False
    impl = BLOB(DB_STR_BLOB_MAXLEN_STORED)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.engine = SecureMessage(
            pass_key=settings.api.encryption_key,
            salt=settings.api.encryption_salt,
        )

    def process_bind_param(self, value: List[str] | None, dialect: Dialect) -> bytes:
        processed_value: str
        if value is not None:
            for scope in value:
                if not scope_regex.fullmatch(scope.lower()):
                    raise ValueError("invalid scope format")
            processed_value = ",".join(value)
        else:
            processed_value = ""
        if len(processed_value) > DB_STR_BLOB_MAXLEN_INPUT:
            raise ValueError("EncryptedScopes too long")
        stored_value = self.engine.sign_and_encrypt(processed_value)
        return stored_value.encode("utf-8")

    def process_result_value(self, value: Any | None, dialect: Dialect) -> List[str]:
        if value is not None:
            if isinstance(value, bytes) and len(value) > 0:
                decrypted_value = self.engine.decrypt_and_verify(
                    value.decode("utf-8"), str
                )
                return str(decrypted_value).split(",")
        return []
