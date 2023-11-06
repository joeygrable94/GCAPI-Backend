import pytest
from pydantic import ValidationError

from app.core.security.schemas import EncryptedMessage, PlainMessage


def test_plain_message() -> None:
    # Test valid input
    message = "Hello, world!"
    plain_message = PlainMessage(message=message)
    assert plain_message.message == message

    # Test empty message
    with pytest.raises(ValidationError):
        PlainMessage(message="")

    # Test message with more than 2048 characters
    with pytest.raises(ValidationError):
        PlainMessage(message="a" * 2049)


def test_encrypted_message() -> None:
    # Test valid input
    message = "Hello, world!"
    encrypted_message = EncryptedMessage(message=message)
    assert encrypted_message.message == message

    # Test empty message
    with pytest.raises(ValidationError):
        EncryptedMessage(message="")

    # Test message with more than 5000 characters
    with pytest.raises(ValidationError):
        EncryptedMessage(message="a" * 5001)
