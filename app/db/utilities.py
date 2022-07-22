import re
import uuid
from datetime import datetime
from typing import Any, Dict, Generator, Optional

from pydantic import UUID4


def _get_date() -> datetime:
    return datetime.now()


def _get_uuid() -> UUID4:
    return uuid.uuid4()


# regex meaning
# checks to confirm a valid email address
email_pattern: re.Pattern = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
)
