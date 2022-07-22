import re
from typing impory Any, Dict, Optional


# https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
# regex meaning
# first str before ':' should only be in a-z, 0-9, -, _
# second or after str after first ':' should only be in a-z, 0-9, -, _, @, .
# ':some_str' should appear at least 1, and can appear more than 1
scope_regex: re.Pattern = re.compile(r"^[a-z0-9-_]+(:[a-z0-9-_@.]+)+$")


class Scope(str):
    @classmethod
    def __get_validators__(cls: Any) -> Generator:
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls: Any, field_schema: Dict[str, Any]) -> None:
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            # some example scopes
            examples=["role:admin", "upload:project:dataset"],
        )

    @classmethod
    def validate(cls: Any, v: str) -> str:
        if not isinstance(v, str):
            raise TypeError("string required")
        m: Optional[re.Match] = scope_regex.fullmatch(v.lower())
        if not m:
            raise ValueError("invalid scope format")
        # you could also return a string here which would mean model.scope
        # would be a string, pydantic won't care but you could end up with some
        # confusion since the value's type won't match the type annotation
        # exactly
        return cls(m.group(0))

    def __repr__(self) -> str:
        return f"Scope({super().__repr__()})"
