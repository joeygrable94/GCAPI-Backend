#!/usr/bin/env python3
# Copyright (C) 2021-2023 All rights reserved.
# FILENAME:  __init__.py
# VERSION: 	 0.3.2
# CREATED: 	 2020-11-25 14:35
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
FastAPI extension that provides Csrf Protection Token support
"""

__version__ = "0.3.2"


from pydantic import BaseModel, StrictStr

from .controller import CsrfProtect
from .errors import CsrfProtectError
from .exceptions import configure_csrf_exceptions
from .schemas import CsrfToken
from .settings import csrf_settings


class CsrfSettings(BaseModel):
    cookie_key: StrictStr = csrf_settings.csrf_name_key
    header_name: StrictStr = csrf_settings.csrf_header_key
    header_type: StrictStr | None = None
    secret_key: StrictStr = csrf_settings.csrf_secret_key
    token_key: StrictStr = csrf_settings.csrf_name_key


__all__: list[str] = [
    "CsrfSettings",
    "CsrfProtect",
    "configure_csrf_exceptions",
    "CsrfProtectError",
    "CsrfToken",
]
