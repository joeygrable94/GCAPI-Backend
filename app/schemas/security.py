from pydantic import BaseModel


class CsrfToken(BaseModel):
    csrf_token: str


class RateLimitedToken(BaseModel):
    call: bool
    ttl: int
