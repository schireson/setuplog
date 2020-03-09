import tempfile

from setuplog import log, M, setup_logging


def log_levels(logger):
    logger.info("")
    logger.warning("")
    logger.error("")


def log_multiple_lines(logger):
    logger.info(
        """
            First line
            Second line
            Third line
        """
    )


def test_setup_logging(capsys):
    setup_logging("INFO")

    log_levels(log)
    console_out, _ = capsys.readouterr()
    assert "INFO" in console_out
    assert "WARNING" in console_out
    assert "ERROR" in console_out


def test_setup_logging_higher_level(capsys):
    setup_logging("WARNING")

    log_levels(log)
    console_out, _ = capsys.readouterr()
    assert "INFO" not in console_out
    assert "WARNING" in console_out
    assert "ERROR" in console_out


def test_setup_logging_escape_unicode(capsys):
    setup_logging("INFO")

    log_multiple_lines(log)
    console_out, _ = capsys.readouterr()
    assert "\n" in console_out
    assert "\\n" not in console_out

    setup_logging("INFO", escape_unicode=True)

    log_multiple_lines(log)
    console_out, _ = capsys.readouterr()
    assert "\\n" in console_out


def test_setup_file_logging(capsys):
    f = tempfile.NamedTemporaryFile(mode="r+")
    setup_logging("INFO", log_file=f.name)

    log_levels(log)

    console_out, _ = capsys.readouterr()
    assert "INFO" in console_out
    assert "WARNING" in console_out
    assert "ERROR" in console_out

    file = f.read()
    assert "INFO" in file
    assert "WARNING" in file
    assert "ERROR" in file


def test_no_namespace(capsys):
    setup_logging()

    log.info("woah!")

    console_out, _ = capsys.readouterr()
    assert " - test_logger - INFO - woah!" in console_out


def test_namespace(capsys):
    setup_logging(namespace="foo")

    log.info("woah!")

    console_out, _ = capsys.readouterr()
    assert " - foo.test_logger - INFO - woah!" in console_out


def test_M(capsys):
    setup_logging(namespace="foo")

    log.info(M("{0} {woah}!", "hi", woah="there"))

    console_out, _ = capsys.readouterr()
    assert "hi there" in console_out


def test_exception_formatting(capsys):
    setup_logging(namespace="foo")

    try:
        raise Exception("wat")
    except Exception:
        log.info("msg", exc_info=True)

    console_out, _ = capsys.readouterr()
    assert "wat" in console_out
