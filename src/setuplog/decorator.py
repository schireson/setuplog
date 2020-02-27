import functools
import time
from setuplog.logger import log
import contextlib


def log_exceptions(logger):
    """Log exceptions in the decorated function and its nested calls.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                log.exception("")
                raise

        return wrapper

    return decorator


@contextlib.contextmanager
def log_duration(action):
    log.info("Started: %s", action)
    start_time = time.time()

    try:
        yield
    except Exception:
        end_time = time.time()
        duration = end_time - start_time

        log.info("Failed: %s (in %.1f seconds)", action, duration)
        raise
    else:
        end_time = time.time()
        duration = end_time - start_time

    log.info("Completed: %s (in %.1f seconds)", action, duration)
