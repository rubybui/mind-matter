from functools import wraps
from flask import request, abort
from mind_matter_api.utils.auth import get_authenticated_user_id_or_abort, is_user_admin, is_user_owner

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = get_authenticated_user_id_or_abort()
        return f(user_id, *args, **kwargs)
    return decorated

def require_admin(f):
    @wraps(f)
    def decorated(user_id, *args, **kwargs):
        if not is_user_admin(user_id):
            abort(403, description="Admin privileges required")
        return f(user_id, *args, **kwargs)
    return decorated

def require_owner(resource_getter):
    def decorator(f):
        @wraps(f)
        def decorated(user_id, *args, **kwargs):
            resource = resource_getter(*args, **kwargs)
            if not is_user_owner(user_id, resource) and not is_user_admin(user_id):
                abort(403, description="Permission denied")
            return f(user_id, resource, *args, **kwargs)
        return decorated
    return decorator
