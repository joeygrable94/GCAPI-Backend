from re import Pattern, compile

# https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
# first str before ':' should only be in a-z, 0-9, -, _
# second or after str after first ':' should only be in a-z, 0-9, -, _, @, .
# ':some_str' should appear at least 1, and can appear more than 1
scope_regex: Pattern = compile(r"^[a-z0-9-_]+(:[a-z0-9-_@.]+)+$")


class Scope(str):
    def __new__(self, value: str) -> "Scope":
        m = scope_regex.fullmatch(value.lower())
        if not m:
            raise ValueError("invalid scope format")
        return super().__new__(self, m.group(0))


class AclPermission(Scope):
    pass


class AclPrivilege(Scope):
    pass
