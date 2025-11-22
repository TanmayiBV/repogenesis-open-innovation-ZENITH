from functools import lru_cache
from datetime import datetime, timedelta
import json

# Simple cache storage
_cache = {}
_cache_expiry = {}

def cache_with_ttl(ttl_seconds=300):
    '''Cache function results with time-to-live'''
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Create cache key
            key = f\"{func.__name__}_{str(args)}_{str(kwargs)}\"
            
            # Check if cached and not expired
            if key in _cache:
                if datetime.now() < _cache_expiry[key]:
                    print(f'✅ Cache hit: {func.__name__}')
                    return _cache[key]
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            _cache[key] = result
            _cache_expiry[key] = datetime.now() + timedelta(seconds=ttl_seconds)
            
            return result
        return wrapper
    return decorator

def clear_cache():
    '''Clear all cached data'''
    global _cache, _cache_expiry
    _cache = {}
    _cache_expiry = {}
    print('✅ Cache cleared')
