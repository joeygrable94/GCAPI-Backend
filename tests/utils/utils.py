import random
import string
from datetime import datetime
from faker.providers.internet import Provider as InternetProvider

now = datetime.now()
random.seed(int(round(now.timestamp())))


def random_boolean() -> bool:
    return bool(random.getrandbits(1))


def random_lower_string(chars: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=chars))


def random_email() -> str:
    return f"{random_lower_string()}@getcommunity.com"


def random_domain(chars: int = 16, top_level: str = "com") -> str:
    return InternetProvider.domain_name()
    # return "".join(random.choices(string.ascii_lowercase, k=chars)) + "." + top_level
