"""Implement suggested strategy of python docs.

https://docs.python.org/3/howto/logging-cookbook.html#use-of-alternative-formatting-styles
"""
import logging


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
        try:
            return self.fmt.format(*self.args, **self.kwargs)
        except Exception:
            return str(self.fmt)


class StyleAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        super(StyleAdapter, self).__init__(logger, extra or {})

    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            self.logger._log(level, M(msg, *args, **kwargs), ())
