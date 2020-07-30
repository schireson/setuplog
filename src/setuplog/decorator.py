import contextlib
import functools
import logging
import time

from setuplog.adaptors import M
from setuplog.logger import log


def log_exceptions(func):
    """Log exceptions in the decorated function and its nested calls.

    Examples:
        >>> @log_exceptions
        ... def err():
        ...     raise Exception("ack!")
    """

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.exception("")
            raise

    return decorator


@contextlib.contextmanager
def log_duration(action: str, level=logging.INFO):
    """Log the duration of the callee.

    Args:
        action: A description of the action being performed by the callee.

    Examples:
        >>> import time
        >>> @log_duration('sleeping')
        ... def sleeping():
        ...     time.sleep(.1)
    """
    log.info(M("Started: {}", action))
    start_time = time.time()

    try:
        yield
    except Exception:
        end_time = time.time()
        duration = end_time - start_time

        log.info(M("Failed: {} (in {:.1f} seconds)", action, duration))
        raise
    else:
        end_time = time.time()
        duration = end_time - start_time

    log.info(M("Completed: {} (in {:.1f} seconds)", action, duration))
