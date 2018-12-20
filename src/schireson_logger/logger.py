import logging
import sys


def setup_logging(
        log_level,
        log_file=None,
        logger_name='logger',
        log_format=None,
        date_format=None,
        additional_loggers=None
):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    console_handler = logging.StreamHandler(stream=sys.stdout)

    if not log_format:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    if not date_format:
        date_format = '%Y-%m-%d %H:%M:%S'

    formatter = logging.Formatter(log_format, date_format)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if additional_loggers:
        for additional_logger in additional_loggers:
            new_logger = logging.getLogger(additional_logger)
            new_logger.setLevel(log_level)
            if log_file:
                new_logger.addHandler(file_handler)
