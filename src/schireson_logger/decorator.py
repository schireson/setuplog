from functools import wraps


def log_exceptions(logger):
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
