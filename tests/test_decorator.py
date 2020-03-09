import pytest

from setuplog import log, log_duration, log_exceptions, setup_logging


def test_log_exceptions(capsys):
    setup_logging("INFO")

    @log_exceptions
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


def test_log_duration_success(capsys):
    setup_logging("INFO")

    @log_duration("function")
    def function():
        print("wahoo")

    function()

    console_out, _ = capsys.readouterr()
    assert "Completed: function" in console_out


def test_log_duration_error(capsys):
    setup_logging("INFO")

    @log_duration("bad function")
    def divide_by_zero():
        return 1 / 0

    with pytest.raises(ZeroDivisionError):
        divide_by_zero()

    console_out, _ = capsys.readouterr()
    assert "Failed: bad function" in console_out
