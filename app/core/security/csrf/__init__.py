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

from .core import CsrfProtect
from .exceptions import CsrfProtectError

__all__: List[str] = [
    "CsrfProtect",
    "CsrfProtectError",
]
