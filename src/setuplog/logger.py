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


def create_log_handler(name, log_level=None, style_adaptor=None):
    """Create a logger.
    """
    log = logging.getLogger(name)

    if log_level:
        log.setLevel(log_level)

    if style_adaptor:
        log = style_adaptor(log)

    return log


class _Logging(object):
    def __getattr__(self, attr):
        segments = []
        namespace = getattr(logging.config, "namespace", "")
        if namespace:
            segments.append(namespace)

        style_adaptor = getattr(logging.config, "style_adaptor", None)

        # Ensure the logger name is pulled from 1 frame up rather than from the local frame.
        frame_name = sys._getframe(1).f_globals["__name__"]
        segments.append(frame_name)

        name = ".".join(segments)
        logger = _cached_logger(name, style_adaptor=style_adaptor)
        return getattr(logger, attr)


_cached_logger = lru_cache()(create_log_handler)
log = _Logging()
