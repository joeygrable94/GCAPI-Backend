from re import Pattern, compile

# checks to confirm a valid email address
email_regex: Pattern = compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

# https://stackoverflow.com/questions/46582497/python-regex-for-password-validation
# - at least one digit
# - one uppercase letter
# - at least one lowercase letter
# - at least one special character
pw_req_regex: Pattern = compile(
    r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$"
)

# A regex that matches a domain name.
domain_name_regex: Pattern = compile(
    r"^(((?!\-))(xn\-\-)?[a-z0-9\-_]{0,61}[a-z0-9]{1,1}\.)*(xn\-\-)?([a-z0-9\-]{1,61}|[a-z0-9\-]{1,30})\.[a-z]{2,}$"  # noqa: E501
)
domain_in_url_regex: Pattern = compile(
    r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)"
)

# https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
# first str before ':' should only be in a-z, 0-9, -, _
# second or after str after first ':' should only be in a-z, 0-9, -, _, @, .
# ':some_str' should appear at least 1, and can appear more than 1
scope_regex: Pattern = compile(r"^[a-z0-9-_]+(:[a-z0-9-_@.]+)+$")
