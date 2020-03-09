import sys
from setuplog.formatters import UnicodeEscapeFormatter


def test_format_exception():
    try:
        raise Exception("foo")
    except Exception:
        info = sys.exc_info()
        result = UnicodeEscapeFormatter().formatException(info)

    assert "Traceback (most recent call last):" in result
    assert "Exception: foo" in result
