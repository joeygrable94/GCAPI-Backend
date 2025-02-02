from pydantic import BaseModel


class RateLimitedToken(BaseModel):
    call: bool
    ttl: int
