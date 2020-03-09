from __future__ import absolute_import

import logging
import logging.config
import logging.handlers

from setuplog.adaptors import StyleAdapter
from setuplog.formatters import UnicodeEscapeFormatter

_DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
_DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_DEFAULT_LOG_LEVEL_OVERRIDES = {"requests": "INFO"}
_FILE_HANDLER_MAX_BYTES = 1048576


def generate_loggers(*, log_level_overrides):
    loggers = {}
    for logger, new_level in log_level_overrides.items():
        loggers[logger] = {"level": new_level}
    return loggers


def generate_handlers(level, formatter, *, log_file=None):
    handlers = {
        "main": {
            "class": "logging.StreamHandler",
            "formatter": formatter,
            "stream": "ext://sys.stdout",
            "level": level,
        }
    }
    if log_file:
        handlers["file_handler"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": formatter,
            "filename": log_file,
            "maxBytes": _FILE_HANDLER_MAX_BYTES,
            "level": level,
        }
    return handlers


def generate_logging_config(
    level,
    formatter,
    format_=_DEFAULT_FORMAT,
    date_format=_DEFAULT_DATE_FORMAT,
    log_level_overrides=_DEFAULT_LOG_LEVEL_OVERRIDES,
    log_file=None,
):
    loggers = generate_loggers(log_level_overrides=log_level_overrides)
    handlers = generate_handlers(level, formatter, log_file=log_file)

    return {
        "version": 1,
        "formatters": {
            "main": {"format": format_, "datefmt": date_format},
            "escaped": {"()": UnicodeEscapeFormatter, "format": format_, "datefmt": date_format},
        },
        "disable_existing_loggers": False,
        "handlers": handlers,
        "loggers": loggers,
        "root": {"level": "WARNING", "handlers": list(handlers.keys())},
    }


def get_style_adaptor(style: str):
    if style == "format":
        return StyleAdapter
    else:
        return None


def setup_logging(
    log_level=logging.INFO,
    escape_unicode=False,
    namespace=None,
    log_format=_DEFAULT_FORMAT,
    date_format=_DEFAULT_DATE_FORMAT,
    log_level_overrides=_DEFAULT_LOG_LEVEL_OVERRIDES,
    log_file=None,
    style="percent",
):
    """Set up logging for a file or a project.

    The param log_level_overrides is a mapping of loggers to levels, to set levels for dependent packages,
    e.g. ``{'requests': 'INFO'}``
    """
    logging.config.namespace = namespace

    if namespace:
        log_level_overrides.update({namespace: log_level})

    formatter = "main"
    if escape_unicode:
        formatter = "escaped"

    logging_config = generate_logging_config(
        log_level,
        format_=log_format,
        date_format=date_format,
        log_level_overrides=log_level_overrides,
        formatter=formatter,
        log_file=log_file,
    )

    logging.config.style_adaptor = get_style_adaptor(style)

    logging.config.dictConfig(logging_config)