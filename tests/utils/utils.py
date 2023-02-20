from datetime import datetime
import random
import string

now = datetime.now()
random.seed(int(round(now.timestamp())))


def random_boolean() -> bool:
    return bool(random.getrandbits(1))


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@getcommunity.com"
