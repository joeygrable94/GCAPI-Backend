from re import Pattern, compile

from pydantic import BaseModel, Field

# https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
# first str before ':' should only be in a-z, 0-9, -, _
# second or after str after first ':' should only be in a-z, 0-9, -, _, @, .
# ':some_str' should appear at least 1, and can appear more than 1
scope_regex: Pattern = compile(r"^[a-z0-9-_]+(:[a-z0-9-_@.]+)+$")


class AclScope(BaseModel):
    scope: str = Field(..., pattern=scope_regex.pattern)

    def __repr__(self) -> str:
        return f"Scope({self.scope})"
