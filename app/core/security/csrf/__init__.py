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

from typing import List

from pydantic import BaseModel, StrictStr

from app.core.config import settings

from .core import CsrfProtect
from .exceptions import CsrfProtectError, configure_csrf_exceptions


class CsrfSettings(BaseModel):
    cookie_key: StrictStr = settings.api.csrf_name_key
    header_name: StrictStr = settings.api.csrf_header_key
    header_type: StrictStr | None = None
    secret_key: StrictStr = settings.api.csrf_secret_key
    token_key: StrictStr = settings.api.csrf_name_key


__all__: List[str] = [
    "CsrfProtect",
    "CsrfSettings",
    "CsrfProtectError",
    "configure_csrf_exceptions",
]
