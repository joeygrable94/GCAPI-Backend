from datetime import datetime

from pydantic import BaseModel, Field


class ClerkUser(BaseModel):
    auth_id: str | None = Field(alias="user_id")
    email: str = Field("")
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    username: str | None = Field(None)
    picture: str | None = Field(None)
    is_verified: bool | None = Field(False)
    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
