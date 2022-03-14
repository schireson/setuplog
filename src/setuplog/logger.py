"""Automatically prepare a logger for the current module.

>>> from setuplog import log
>>>
>>> log.debug('debug!')
>>> log.info('info!')
>>> log.warning('warning!')
>>> log.error('error!')
"""
from __future__ import absolute_import

import logging
import logging.config
import sys
from functools import lru_cache
from typing import Any, Union

from setuplog.adaptors import M


def create_log_handler(name, log_level=None, style_adaptor=None):
    """Create a logger.
    """
    log = logging.getLogger(name)

    if log_level:
        log.setLevel(log_level)

    if style_adaptor:
        log = style_adaptor(log)

    return log


def get_logger() -> logging.Logger:
    segments = []
    namespace = getattr(logging.config, "namespace", "")
    if namespace:
        segments.append(namespace)

    style_adaptor = getattr(logging.config, "style_adaptor", None)

    # Ensure the logger name is pulled from 2 frames up rather than from the local frame. One frame for this function, and one for the
    # `_Logging` function calls.
    frame_name = sys._getframe(2).f_globals["__name__"]
    segments.append(frame_name)

    name = ".".join(segments)
    return _cached_logger(name, style_adaptor=style_adaptor)


class _Logging(object):
    def debug(self, msg: Union[object, str, M], *args: Any, **kwargs: Any) -> None:
        logger = get_logger()
        logger.debug(msg, *args, **kwargs)

    def info(self, msg: Union[object, str, M], *args: Any, **kwargs: Any) -> None:
        logger = get_logger()
        logger.info(msg, *args, **kwargs)

    def warning(self, msg: Union[object, str, M], *args: Any, **kwargs: Any) -> None:
        logger = get_logger()
        logger.warning(msg, *args, **kwargs)

    def error(self, msg: Union[object, str, M], *args: Any, **kwargs: Any) -> None:
        logger = get_logger()
        logger.error(msg, *args, **kwargs)

    def exception(self, msg: Union[object, str, M], *args: Any, exc_info=True, **kwargs: Any) -> None:
        logger = get_logger()
        logger.exception(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg: Union[object, str, M], *args: Any, **kwargs: Any) -> None:
        logger = get_logger()
        logger.critical(msg, *args, **kwargs)

    def log(self, level: int, msg: Union[object, str, M], *args: Any, **kwargs: Any) -> None:
        logger = get_logger()
        logger.log(level, msg, *args, **kwargs)


_cached_logger = lru_cache()(create_log_handler)
log = _Logging()
