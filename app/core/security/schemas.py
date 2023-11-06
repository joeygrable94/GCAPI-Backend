from pydantic import BaseModel, field_validator


class CsrfToken(BaseModel):
    csrf_token: str


class RateLimitedToken(BaseModel):
    call: bool
    ttl: int


class PlainMessage(BaseModel):
    message: str

    @field_validator("message", mode="before")
    def check_message(cls, value: str) -> str:
        if not value:
            raise ValueError("message cannot be empty")
        if len(value) > 2048:
            raise ValueError("message may not contain more than 2048 characters")
        return value


class EncryptedMessage(BaseModel):
    message: str

    @field_validator("message", mode="before")
    def check_message(cls, value: str) -> str:
        if not value:
            raise ValueError("message cannot be empty")
        if len(value) > 5000:
            raise ValueError("message may not contain more than 5000 characters")
        return value
