import random
import string

from pydantic import EmailStr


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> EmailStr:
    return f"{random_lower_string()}@getcommunity.com"
