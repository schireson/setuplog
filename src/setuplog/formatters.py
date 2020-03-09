import logging


class UnicodeEscapeFormatter(logging.Formatter):
    def escape_str(self, string):
        return string.encode("unicode_escape").decode("utf-8")

    def formatException(self, exc_info):
        result = super(UnicodeEscapeFormatter, self).formatException(exc_info)
        return self.escape_str(result)

    def format(self, record):
        result = super(UnicodeEscapeFormatter, self).format(record)
        return self.escape_str(result)
