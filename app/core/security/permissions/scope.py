from typing import NewType

"""
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
"""

Scope = NewType("Scope", str)
AclPermission = NewType("AclPermission", str)
AclPrivilege = NewType("AclPrivilege", str)
