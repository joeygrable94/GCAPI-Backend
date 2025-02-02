from pydantic import BaseModel, field_validator

from app.db.constants import DB_STR_DESC_MAXLEN_INPUT, DB_STR_URLPATH_MAXLEN_INPUT


class PlainMessage(BaseModel):
    message: str

    @field_validator("message", mode="before")
    def check_message(cls, value: str) -> str:
        if not value:
            raise ValueError("message cannot be empty")
        if len(value) > DB_STR_URLPATH_MAXLEN_INPUT:
            raise ValueError(
                f"message may not contain more than {DB_STR_URLPATH_MAXLEN_INPUT} characters"
            )
        return value


class EncryptedMessage(BaseModel):
    message: str

    @field_validator("message", mode="before")
    def check_message(cls, value: str) -> str:
        if not value:
            raise ValueError("message cannot be empty")
        if len(value) > DB_STR_DESC_MAXLEN_INPUT:
            raise ValueError(
                f"message may not contain more than {DB_STR_DESC_MAXLEN_INPUT} characters"
            )
        return value
