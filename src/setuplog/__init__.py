from setuplog.adaptors import M, StyleAdapter
from setuplog.decorator import log_duration, log_exceptions
from setuplog.logger import create_log_handler, log
from setuplog.setup import setup_logging

__all__ = [
    "create_log_handler",
    "log",
    "log_duration",
    "log_exceptions",
    "M",
    "setup_logging",
    "StyleAdapter",
]
