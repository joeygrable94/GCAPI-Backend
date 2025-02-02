from pydantic import BaseModel


class CsrfToken(BaseModel):
    csrf_token: str
