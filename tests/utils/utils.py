import random
import string
from datetime import _Date, datetime

from pydantic import EmailStr

now = datetime.now()
random.seed(int(round(now.timestamp())))


def random_boolean() -> bool:
    return bool(random.getrandbits(1))


def random_integer() -> int:
    return random.randint(1, 1000)


def random_float() -> float:
    return random.uniform(1.0, 1000.0)


def random_datetime() -> datetime:
    return datetime.now()


def random_date() -> _Date:
    return datetime.date(datetime.now())


def random_lower_string(chars: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=chars))


def random_email() -> EmailStr:
    return f"{random_lower_string()}@getcommunity.com"


def random_domain(chars: int = 16, top_level: str = "com") -> str:
    return "".join(random.choices(string.ascii_lowercase, k=chars)) + "." + top_level
