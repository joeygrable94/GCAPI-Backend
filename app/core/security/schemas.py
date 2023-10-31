from pydantic import BaseModel, field_validator


class CsrfToken(BaseModel):
    csrf_token: str


class RateLimitedToken(BaseModel):
    call: bool
    ttl: int


class PlainMessage(BaseModel):
    message: str


class EncryptedMessage(BaseModel):
    message: str


class RSAEncryptMessage(BaseModel):
    message: str

    @field_validator("message")
    def check_message(cls, value: str) -> str:  # pragma: no cover
        if not value:
            raise ValueError("message cannot be empty")
        if len(value) > 53:
            raise ValueError("message may not contain more than 53 characters")
        return value


class RSADecryptMessage(BaseModel):
    message: str

    @field_validator("message")
    def check_message(cls, value: str) -> str:  # pragma: no cover
        if not value:
            raise ValueError("message cannot be empty")
        if len(value) > 128:
            raise ValueError("message may not contain more than 128 characters")
        return value
