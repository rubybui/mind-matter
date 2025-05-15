import logging
from flask import request, abort, current_app as app
from mind_matter_api.models import User
from mind_matter_api.services.users import UserService
from mind_matter_api.repositories.users import UserRepository

logging.basicConfig(level=logging.DEBUG)

def get_user_id_from_token(token):
    try:
        user_id = User.decode_auth_token(str(token))
        return user_id
    except Exception as e:
        logging.error(f"Token decoding failed: {str(e)}")
        return None

def get_authenticated_user_id_or_abort():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        abort(401, description="Authorization token required")

    token = auth_header.split(" ")[1]
    user_id = get_user_id_from_token(token)
    if not user_id:
        abort(401, description="Invalid or expired token")

    return user_id

def is_user_admin(user_id):
    try:
        user_repository = UserRepository()
        user_service = UserService(user_repository)
        user = user_service.get_user(user_id)
        is_admin = user is not None and user.role == "admin"
        return is_admin
    except Exception as e:
        logging.error(f"[is_user_admin] Admin check failed for user_id={user_id}: {e}")
        return False

def is_user_owner(user_id, resource):
    try:

        if resource is None:
            return False
            
        # Get the user_id attribute directly from the SQLAlchemy model
        resource_user_id = getattr(resource, "user_id", None)
        # Convert both IDs to integers for comparison
        try:
            # Convert user_id to int if it's a string
            user_id_int = int(user_id) if isinstance(user_id, str) else user_id
            resource_user_id_int = int(resource_user_id) if resource_user_id is not None else None

            is_owner = resource_user_id_int == user_id_int
            return is_owner
        except (ValueError, TypeError) as e:
            app.logger.error(f"[is_user_owner] Error converting IDs to integers: {e}")
            app.logger.error(f"[is_user_owner] user_id type: {type(user_id)}, value: {user_id}")
            app.logger.error(f"[is_user_owner] resource_user_id type: {type(resource_user_id)}, value: {resource_user_id}")
            return False
            
    except Exception as e:
        logging.error(f"[is_user_owner] Ownership check failed: {e}")
        return False
