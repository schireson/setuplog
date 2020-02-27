from __future__ import absolute_import
import logging
import logging.config
import logging.handlers
import sys
from functools import lru_cache


_DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
_DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_DEFAULT_LOG_LEVEL_OVERRIDES = {"requests": "INFO"}
_FILE_HANDLER_MAX_BYTES = 1048576


class UnicodeEscapeFormatter(logging.Formatter):
    def escape_str(self, string):
        return string.encode("unicode_escape").decode("utf-8")

    def formatException(self, exc_info):
        result = super(UnicodeEscapeFormatter, self).formatException(exc_info)
        return self.escape_str(result)

    def format(self, record):
        result = super(UnicodeEscapeFormatter, self).format(record)
        return self.escape_str(result)


class M:
    """Support format strings.

    >>> import logging
    >>> logging.info(M('foo={foo}', foo=1))
    """

    def __init__(self, fmt, *args, **kwargs):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.fmt.format(*self.args, **self.kwargs)


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


_logging_namespace = None


def setup_logging(
    log_level=logging.INFO,
    escape_unicode=False,
    namespace=None,
    log_format=_DEFAULT_FORMAT,
    date_format=_DEFAULT_DATE_FORMAT,
    log_level_overrides=_DEFAULT_LOG_LEVEL_OVERRIDES,
    log_file=None,
):
    """Set up logging for a file or a project.

    The param log_level_overrides is a mapping of loggers to levels, to set levels for dependent packages,
    e.g. ``{'requests': 'INFO'}``
    """
    global _logging_namespace
    _logging_namespace = namespace

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

    logging.config.dictConfig(logging_config)


def create_log_handler(name, log_level="DEBUG"):
    """Create a logger.
    """
    log = logging.getLogger(name)
    log.setLevel(log_level)
    return log


class _Logging(object):
    def __getattr__(self, attr):
        prefix = ""
        if _logging_namespace:
            prefix = _logging_namespace + "."

        # Ensure the logger name is pulled from 1 frame up rather than from the local frame.
        logger = _cached_logger(prefix + sys._getframe(1).f_globals["__name__"])
        return getattr(logger, attr)


_cached_logger = lru_cache()(create_log_handler)
log = _Logging()
