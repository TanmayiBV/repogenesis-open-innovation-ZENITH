import functools
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_errors(func):
    '''Decorator to handle errors in backend functions'''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'Error in {func.__name__}: {str(e)}')
            return {'status': 'error', 'message': str(e)}
    return wrapper

# Example usage:
# @handle_errors
# def some_function():
#     pass
