#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
levels: 'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
CRITICAL    50
ERROR       40
WARNING     30
INFO        20
DEBUG       10
NOTSET      0
"""


__author__ = "Tzury Bar Yochay"
__version__ = "0.1"
__license__ = "GPLv3"

import logging
from typing import Any

from app.core.config import settings


class Color:
    """
    The color mechanism is taken from Scapy:
    http://www.secdev.org/projects/scapy/
    Thanks to Philippe Biondi for his awesome tool and design.
    """

    normal: str = "\033[0m"
    black: str = "\033[30m"
    red: str = "\033[31m"
    green: str = "\033[32m"
    yellow: str = "\033[33m"
    blue: str = "\033[34m"
    purple: str = "\033[35m"
    cyan: str = "\033[36m"
    grey: str = "\033[37m"
    bold: str = "\033[1m"
    uline: str = "\033[4m"
    blink: str = "\033[5m"
    invert: str = "\033[7m"


class ColorTheme:
    def __repr__(self) -> str:  # pragma: no cover
        return "<%s>" % self.__class__.__name__

    def __getattr__(self, attr: Any) -> Any:  # pragma: no cover
        return lambda x: x


class NoTheme(ColorTheme):
    pass


class AnsiColorTheme(ColorTheme):  # pragma: no cover
    def __getattr__(self, attr: Any) -> Any:
        if attr.startswith("__"):
            raise AttributeError(attr)
        s: Any = "style_%s" % attr
        if s in self.__class__.__dict__:
            before: Any = getattr(self, s)
            after: Any = self.style_normal
        else:
            before = ""
            after = ""

        def do_style(
            val: Any, fmt: Any = None, before: Any = before, after: Any = after
        ) -> Any:
            if fmt is None:
                if not isinstance(val, str):
                    val = str(val)
            else:
                val = fmt % val
            return before + val + after

        return do_style

    style_normal: str = ""
    style_prompt: str = ""  # '>>>'
    style_punct: str = ""
    style_id: str = ""
    style_not_printable: str = ""
    style_class_name: str = ""
    style_field_name: str = ""
    style_field_value: str = ""
    style_emph_field_name: str = ""
    style_emph_field_value: str = ""
    style_watchlist_name: str = ""
    style_watchlist_type: str = ""
    style_watchlist_value: str = ""
    style_fail: str = ""
    style_success: str = ""
    style_odd: str = ""
    style_even: str = ""
    style_yellow: str = ""
    style_active: str = ""
    style_closed: str = ""
    style_left: str = ""
    style_right: str = ""


class BlackAndWhite(AnsiColorTheme):
    pass


class DefaultTheme(AnsiColorTheme):
    style_normal: str = Color.normal
    style_prompt: str = Color.blue + Color.bold
    style_punct: str = Color.normal
    style_id: str = Color.blue + Color.bold
    style_not_printable: str = Color.grey
    style_class_name: str = Color.red + Color.bold
    style_field_name: str = Color.blue
    style_field_value: str = Color.purple
    style_emph_field_name: str = Color.blue + Color.uline + Color.bold
    style_emph_field_value: str = Color.purple + Color.uline + Color.bold
    style_watchlist_type: str = Color.blue
    style_watchlist_value: str = Color.purple
    style_fail: str = Color.red + Color.bold
    style_success: str = Color.blue + Color.bold
    style_even: str = Color.black + Color.bold
    style_odd: str = Color.black
    style_yellow: str = Color.yellow
    style_active: str = Color.black
    style_closed: str = Color.grey
    style_left: str = Color.blue + Color.invert
    style_right: str = Color.red + Color.invert


default_theme: DefaultTheme = DefaultTheme()


class Logger:
    def __init__(
        self, name: str = settings.api.logger_name, level: str = "INFO"
    ) -> None:
        # exception
        self.file_frmt: logging.Formatter = logging.Formatter(
            "%(levelname)-11s\b%(asctime)s %(name)s:%(lineno)d %(message)s"  # noqa: E501
        )
        self.stream_frmt: logging.Formatter = logging.Formatter(
            "%(levelname)-11s\b%(asctime)-6s %(name)s:%(lineno)d %(message)s"  # noqa: E501
        )
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(logging.getLevelName(level))
        # file handler
        self.fh: logging.FileHandler = logging.FileHandler(f"{name}.log")
        # stream handler
        self.ch: logging.StreamHandler = logging.StreamHandler()
        # set formatter
        self.fh.setFormatter(self.file_frmt)
        self.ch.setFormatter(self.stream_frmt)
        # add handlers
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)

    def log(self, *args: Any) -> Any:  # pragma: no cover
        self.logger.info(
            default_theme.style_normal
            + "".join(str(i) for i in args)
            + default_theme.style_normal
        )

    def debug(self, *args: Any) -> Any:  # pragma: no cover
        self.logger.debug(
            default_theme.style_prompt
            + "".join(str(i) for i in args)
            + default_theme.style_normal
        )

    def info(self, *args: Any) -> Any:  # pragma: no cover
        self.logger.info(
            default_theme.style_normal
            + "".join(str(i) for i in args)
            + default_theme.style_normal
        )

    def exception(self, *args: Any) -> Any:  # pragma: no cover
        self.logger.exception(
            default_theme.style_fail
            + "".join(str(i) for i in args)
            + default_theme.style_normal
        )

    def warning(self, *args: Any) -> Any:  # pragma: no cover
        self.logger.warning(
            default_theme.style_right
            + "".join(str(i) for i in args)
            + default_theme.style_normal
        )
