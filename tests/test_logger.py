import tempfile

import pytest

from schireson_logger import log_exceptions, setup_logging


def log_levels(logger):
    logger.info('')
    logger.warn('')
    logger.error('')


def log_multiple_lines(logger):
    logger.info(
        """
            First line
            Second line
            Third line
        """
    )


def test_setup_logging(capsys):
    setup_logging('INFO')

    from schireson_logger import log

    log_levels(log)
    console_out, _ = capsys.readouterr()
    assert 'INFO' in console_out
    assert 'WARNING' in console_out
    assert 'ERROR' in console_out


def test_setup_logging_higher_level(capsys):
    setup_logging('WARNING')

    from schireson_logger import log

    log_levels(log)
    console_out, _ = capsys.readouterr()
    assert 'INFO' not in console_out
    assert 'WARNING' in console_out
    assert 'ERROR' in console_out


def test_setup_logging_escape_unicode(capsys):
    setup_logging('INFO')

    from schireson_logger import log

    log_multiple_lines(log)
    console_out, _ = capsys.readouterr()
    assert '\n' in console_out
    assert '\\n' not in console_out

    setup_logging('INFO', escape_unicode=True)

    log_multiple_lines(log)
    console_out, _ = capsys.readouterr()
    assert '\\n' in console_out


def test_setup_file_logging(capsys):
    f = tempfile.NamedTemporaryFile(mode='r+')
    setup_logging('INFO', log_file=f.name)

    from schireson_logger import log

    log_levels(log)

    console_out, _ = capsys.readouterr()
    assert 'INFO' in console_out
    assert 'WARNING' in console_out
    assert 'ERROR' in console_out

    file = f.read()
    assert 'INFO' in file
    assert 'WARNING' in file
    assert 'ERROR' in file


def test_decorator(capsys):
    setup_logging('INFO')

    from schireson_logger import log

    @log_exceptions(log)
    def divide_by_zero():
        return 1 / 0

    log_levels(log)
    with pytest.raises(ZeroDivisionError):
        divide_by_zero()

    console_out, _ = capsys.readouterr()
    assert 'INFO' in console_out
    assert 'WARNING' in console_out
    assert 'ERROR' in console_out
    assert 'Traceback' in console_out
