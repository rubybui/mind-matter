import logging
from flask import request, jsonify
from mind_matter_api.models import User  # Adjust if your path is different
from mind_matter_api.services import UserService

def get_user_id_from_token(token):
    try:
        user_id = User.decode_auth_token(token)
        return user_id
    except Exception as e:
        logging.error(f"Token decoding failed: {str(e)}")
        return None

def get_authenticated_user_id_or_abort():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization token required"}), 401

    token = auth_header.split(" ")[1]
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

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