from __future__ import absolute_import

import logging
import logging.config
import logging.handlers
import sys

if sys.version_info[0] == 3:
    from functools import lru_cache
else:
    from functools32 import lru_cache


class UnicodeEscapeFormatter(logging.Formatter):
    def escape_str(self, string):
        return string.encode('unicode_escape').decode('utf-8')

    def formatException(self, exc_info):
        result = super(UnicodeEscapeFormatter, self).formatException(exc_info)
        return self.escape_str(result)

    def format(self, record):
        result = super(UnicodeEscapeFormatter, self).format(record)
        return self.escape_str(result)


logging_config = {
    'version': 1,
    'formatters': {
        'main': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'escaped': {
            '()': UnicodeEscapeFormatter,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        }
    },
    'disable_existing_loggers': False,
    'handlers': {
        'main': {
            'class': 'logging.StreamHandler',
            'formatter': 'main',
            'stream': 'ext://sys.stdout'
        },
    },
    'loggers': {
        'requests': {
            'level': 'INFO',
            'handlers': ['main'],
            'propagate': False,
        },
        'logger': {
            'level': 'DEBUG',
            'handlers': ['main'],
            'propagate': False,
        },
    },
    'root': {
        'level': 'WARNING',
        'handlers': [
            'main',
        ],
    },
}


def setup_logging(
        log_level,
        log_file=None,
        escape_unicode=False,
        logger_name='logger',
        log_format=None,
        date_format=None,
        log_level_overrides=None,
):
    """Set up logging for a file or a project.

    The param log_level_overrides is a mapping of loggers to levels, to set levels for dependent packages,
    e.g. ``{'requests': 'INFO'}``
    """
    logging_config['handlers']['main']['level'] = log_level

    if log_format:
        logging_config['formatters']['main']['format'] = log_format

    if not date_format:
        date_format = '%Y-%m-%d %H:%M:%S'

    if log_level_overrides:
        for logger, new_level in log_level_overrides.items():
            logging_config['loggers'][logger] = {
                'level': new_level,
                'handlers': ['main'],
                'propagate': False,
            }

    if escape_unicode:
        logging_config['handlers']['main']['formatter'] = 'escaped'

    logging.config.dictConfig(logging_config)

    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=1048576,
            mode='w',
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(
            logging.Formatter(
                logging_config['formatters']['main']['format'],
                date_format
            )
        )

        logging.getLogger(logger_name).addHandler(file_handler)
        if log_level_overrides:
            for logger in log_level_overrides.keys():
                logging.getLogger(logger).addHandler(file_handler)


def create_log_handler(name, log_level='DEBUG'):
    """Create a logger.
    """
    log = logging.getLogger(name)
    log.setLevel(log_level)
    return log


class _Logging(object):
    def __getattr__(self, attr):
        # Ensure the logger name is pulled from 1 frame up rather than from the local frame.
        logger = _cached_logger('logger.' + sys._getframe(1).f_globals['__name__'])
        return getattr(logger, attr)


_cached_logger = lru_cache()(create_log_handler)
log = _Logging()
