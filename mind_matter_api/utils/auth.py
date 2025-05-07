import logging
from flask import request, abort, current_app as app
from mind_matter_api.models import User
from mind_matter_api.services.users import UserService

logging.basicConfig(level=logging.DEBUG)

def get_user_id_from_token(token):
    try:
        user_id = User.decode_auth_token(str(token))
        app.logger.debug(f"uderId: {user_id}")
        return user_id
    except Exception as e:
        logging.error(f"Token decoding failed: {str(e)}")
        return None

def get_authenticated_user_id_or_abort():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        abort(401, description="Authorization token required")

    token = auth_header.split(" ")[1]
    app.logger.debug(f"token: {token}")
    user_id = get_user_id_from_token(token)
    app.logger.debug(f"uderId: {user_id}")
    if not user_id:
        abort(401, description="Invalid or expired token")

    return user_id

def is_user_admin(user_id):
    try:
        user = UserService.get_user(user_id)
        return user is not None and user.role == "admin"
    except Exception as e:
        logging.error(f"Admin check failed for user_id={user_id}: {e}")
        return False

def is_user_owner(user_id, resource):
    try:
        return resource is not None and getattr(resource, "user_id", None) == user_id
    except Exception as e:
        logging.error(f"Ownership check failed: {e}")
        return False
