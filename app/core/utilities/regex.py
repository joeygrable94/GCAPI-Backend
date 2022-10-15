from re import Pattern, compile

# checks to confirm a valid email address
email_regex: Pattern = compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

# https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
# first str before ':' should only be in a-z, 0-9, -, _
# second or after str after first ':' should only be in a-z, 0-9, -, _, @, .
# ':some_str' should appear at least 1, and can appear more than 1
scope_regex: Pattern = compile(r"^[a-z0-9-_]+(:[a-z0-9-_@.]+)+$")

# https://stackoverflow.com/questions/46582497/python-regex-for-password-validation
# - at least one digit
# - one uppercase letter
# - at least one lowercase letter
# - at least one special character
pw_req_regex: Pattern = compile(
    r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$"
)
