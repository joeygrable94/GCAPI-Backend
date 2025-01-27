from pydantic import BaseModel


class ClientAuthorizedUser(BaseModel):
    token_headers: dict[str, str]
    email: str
