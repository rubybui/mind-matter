from functools import wraps
from flask import request, jsonify
from typing import Callable, Any, Dict, List, Optional

def paginate(schema_class=None):
    """
    Decorator to handle pagination for API endpoints.
    
    Args:
        schema_class: Optional schema class to use for serialization
    """
    def decorator(f: Callable):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Get pagination parameters from request
            page = request.args.get('page', type=int, default=1)
            page_size = request.args.get('page_size', type=int, default=10)
            
            # Call the original function with pagination parameters
            result = f(*args, page=page, page_size=page_size, **kwargs)
            
            # If result is a tuple, it contains both data and total count
            if isinstance(result, tuple) and len(result) == 2:
                data, total = result
            else:
                data = result
                total = None
            
            # Format the response
            response = {
                'data': schema_class(many=True).dump(data) if schema_class else data,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': total
                }
            }
            
            return jsonify(response), 200
        return wrapper
    return decorator 