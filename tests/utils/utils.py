import random
import string


def random_boolean() -> bool:
    return bool(random.getrandbits(1))


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@getcommunity.com"


def random_domain() -> str:
    return f"{random_lower_string()}.com"
