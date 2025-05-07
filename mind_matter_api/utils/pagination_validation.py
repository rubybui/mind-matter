from functools import wraps
from flask import abort
from typing import Callable, Any

def validate_pagination_params(f: Callable) -> Callable:
    """
    Decorator to validate pagination parameters.
    Ensures page and page_size are positive integers.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Extract pagination parameters from kwargs
        page = kwargs.get('page', 1)
        page_size = kwargs.get('page_size', 10)
        
        # Validate page
        if not isinstance(page, int) or page < 1:
            abort(400, description="Page must be a positive integer")
            
        # Validate page_size
        if not isinstance(page_size, int) or page_size < 1:
            abort(400, description="Page size must be a positive integer")
            
        return f(*args, **kwargs)
    return wrapper 