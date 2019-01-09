from functools import wraps


def log_exceptions(logger):
    """Log exceptions in the decorated function and its nested calls.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                logger.exception('')
                raise
        return wrapper
    return decorator
