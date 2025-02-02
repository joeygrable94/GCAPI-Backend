import pytest
from pydantic import ValidationError

from app.db.constants import DB_STR_DESC_MAXLEN_INPUT, DB_STR_URLPATH_MAXLEN_INPUT
from app.services.encryption import EncryptedMessage, PlainMessage


def test_plain_message() -> None:
    # Test valid input
    message = "Hello, world!"
    plain_message = PlainMessage(message=message)
    assert plain_message.message == message

    # Test empty message
    with pytest.raises(ValidationError):
        PlainMessage(message="")

    # Test message with more than DB_STR_URLPATH_MAXLEN_INPUT characters
    with pytest.raises(ValidationError):
        PlainMessage(message="a" * (DB_STR_URLPATH_MAXLEN_INPUT + 1))


def test_encrypted_message() -> None:
    # Test valid input
    message = "Hello, world!"
    encrypted_message = EncryptedMessage(message=message)
    assert encrypted_message.message == message

    # Test empty message
    with pytest.raises(ValidationError):
        EncryptedMessage(message="")

    # Test message with more than DB_STR_DESC_MAXLEN_INPUT characters
    with pytest.raises(ValidationError):
        EncryptedMessage(message="a" * (DB_STR_DESC_MAXLEN_INPUT + 1))
