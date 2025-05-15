from functools import wraps
from flask import request, abort, current_app as app
from mind_matter_api.utils.auth import get_authenticated_user_id_or_abort, is_user_admin, is_user_owner
import logging

logging.basicConfig(level=logging.DEBUG)

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
            app.logger.debug(f"[require_owner] Checking ownership for user_id: {user_id}")
            app.logger.debug(f"[require_owner] Args: {args}")
            app.logger.debug(f"[require_owner] Kwargs: {kwargs}")
            
            try:
                resource = resource_getter(*args, **kwargs)
                app.logger.debug(f"[require_owner] Got resource: {resource}")
                
                if not is_user_owner(user_id, resource) and not is_user_admin(user_id):
                    app.logger.debug(f"[require_owner] Permission denied for user {user_id}")
                    abort(403, description="Permission denied")
                
                app.logger.debug(f"[require_owner] Permission granted for user {user_id}")
                return f(user_id, resource, *args, **kwargs)
            except Exception as e:
                app.logger.error(f"[require_owner] Error checking ownership: {str(e)}")
                abort(403, description="Error checking permissions")
        return decorated
    return decorator
