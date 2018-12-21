import logging
import pytest

from schireson_logger import log_exceptions, setup_logging


def log_levels(logger):
    logger.info('')
    logger.warn('')
    logger.error('')


def test_setup_logging(capsys):
    setup_logging('INFO', logger_name='info_logger')
    info_logger = logging.getLogger('info_logger')

    log_levels(info_logger)
    console_out, _ = capsys.readouterr()
    assert 'INFO' in console_out
    assert 'WARN' in console_out
    assert 'ERROR' in console_out


def test_setup_logging_higher_level(capsys):
    setup_logging('WARN', logger_name='warn_logger')
    warn_logger = logging.getLogger('warn_logger')

    log_levels(warn_logger)
    console_out, _ = capsys.readouterr()
    assert 'INFO' not in console_out
    assert 'WARN' in console_out
    assert 'ERROR' in console_out


def test_decorator(capsys):
    setup_logging('INFO', logger_name='exc_logger')
    exc_logger = logging.getLogger('exc_logger')

    @log_exceptions(exc_logger)
    def divide_by_zero():
        return 1 / 0

    log_levels(exc_logger)
    with pytest.raises(ZeroDivisionError):
        divide_by_zero()

    console_out, _ = capsys.readouterr()
    assert 'INFO' in console_out
    assert 'WARN' in console_out
    assert 'ERROR' in console_out
    assert 'Traceback' in console_out
