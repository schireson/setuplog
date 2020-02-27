import pytest

from setuplog.decorator import log_exceptions
from setuplog.logger import setup_logging
from setuplog import log


def test_decorator(capsys):
    setup_logging("INFO")

    @log_exceptions(log)
    def divide_by_zero():
        return 1 / 0

    log.info("")
    log.warning("")
    log.error("")
    with pytest.raises(ZeroDivisionError):
        divide_by_zero()

    console_out, _ = capsys.readouterr()
    assert "INFO" in console_out
    assert "WARNING" in console_out
    assert "ERROR" in console_out
    assert "Traceback" in console_out

