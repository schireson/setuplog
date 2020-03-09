from setuplog import log, setup_logging, M


def test_empty_format(capsys):
    setup_logging(style="format")

    log.info("{}!")
    console_out, _ = capsys.readouterr()
    assert " - INFO - {}!" in console_out


def test_unnamed_format(capsys):
    setup_logging(style="format")

    log.info("{}!", 500)
    console_out, _ = capsys.readouterr()
    assert " - INFO - 500!" in console_out


def test_named_format(capsys):
    setup_logging(style="format")

    log.info("{foo}!", foo=500)
    console_out, _ = capsys.readouterr()
    assert " - INFO - 500!" in console_out


def test_named_and_unnamed_format(capsys):
    setup_logging(style="format")

    log.info("{} {foo}!", "asdf", foo=500)
    console_out, _ = capsys.readouterr()
    assert " - INFO - asdf 500!" in console_out


def test_M(capsys):
    setup_logging(style="format")

    log.info(M("{} {foo}!", "asdf", foo=500))
    console_out, _ = capsys.readouterr()
    assert " - INFO - asdf 500!" in console_out


def test_object(capsys):
    class Foo:
        def __repr__(self):
            return "Foo(1, 2, 3)"

    setup_logging(style="format")

    log.info(Foo())
    console_out, _ = capsys.readouterr()
    assert " - INFO - Foo(1, 2, 3)" in console_out
