from flask import jsonify, request, session
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
import traceback
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from cookbook_api.models import User, db
from mind_matter_api.schemas import UserSchema, UserBodySchema, UserLoginSchema
from mind_matter_api.services.users import UserService
from mind_matter_api.utils.decorators import require_auth, require_owner, require_admin

import logging
logging.basicConfig(level=logging.DEBUG)
# Single and multiple User schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

def init_user_routes(app):

    """
    Initialize user-related API routes.
    """
    @app.route("/users", methods=["GET"])
    @require_auth
    @require_admin
    def get_users():
        """
        Retrieve all users
        ---
        tags:
          - Users
        responses:
          200:
            description: List of users
            schema:
              type: array
              items:
                $ref: '#/definitions/UserSchema'
        """
        user_service: UserService = app.user_service
        users = user_service.get_users()
        return jsonify(users_schema.dump(users)), 200

    @app.route("/users", methods=["POST"])
    def create_user():
        """
        Create a new user
        ---
        tags:
          - Users
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/definitions/UserBodySchema'
        responses:
          201:
            description: User created successfully
            schema:
              $ref: '#/definitions/UserSchema'
          400:
            description: Validation error
        """
        try:
            data = UserBodySchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        with app.app_context():  # Ensures a proper app context
            user_service: UserService = app.user_service
            new_user = user_service.create_user(data)
            token = new_user.encode_auth_token(new_user.user_id)
            return jsonify(user_schema.dump(new_user)), 201

    @app.route("/users/me", methods=["GET"])
    @require_auth
    def get_user(user_id):
        """
        Get the authenticated user's details
        ---
        tags:
          - Users
        responses:
          200:
            description: User details
            schema:
              $ref: '#/definitions/UserSchema'
          404:
            description: User not found
        """
        user_service: UserService = app.user_service
        user = user_service.get_user(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "user": user_schema.dump(user)
        }), 200

    @app.route("/users/me/delete", methods=["DELETE"])
    @require_auth
    def delete_user(user_id):
        """
        Delete the authenticated user's account
        ---
        tags:
          - Users
        responses:
          204:
            description: User account successfully deleted
          404:
            description: User not found
          500:
            description: Internal server error
        """
        try:
            user_service: UserService = app.user_service
            user = user_service.get_user(user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404

            user_service.delete_user(user_id)
            return '', 204
        except Exception as e:
            app.logger.error(f"Error deleting user: {str(e)}")
            return jsonify({"error": "Failed to delete user account"}), 500

    @app.route("/users/register", methods=["POST"])
    def register():
        """
        Register a new user.
        """
        try:
            # Validate request payload
            data = UserBodySchema().load(request.get_json())
            user_service: UserService = app.user_service

            # Check if email already exists
            if not user_service.validate_new_email(data['email']):
                return jsonify({"error": "Email already registered."}), 400

            with app.app_context():
                new_user = user_service.register_user(data)
                token = new_user.encode_auth_token(new_user.user_id)

                app.logger.debug(f"new_user: {new_user}")
                app.logger.debug(f"user dump: {user_schema.dump(new_user)}")
                app.logger.debug(f"token: {token} (type: {type(token)})")

                return jsonify({
                    "user": user_schema.dump(new_user),
                    "token": token
                }), 201

        except ValidationError as err:
            return jsonify({"error": "Validation failed", "messages": err.messages}), 400

        except IntegrityError as e:
            app.logger.error(f"DB Integrity Error: {str(e)}")
            return jsonify({"error": "Email already exists."}), 400

        except Exception as e:
            app.logger.error("Unexpected error:\n" + traceback.format_exc())
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/user/login", methods=["POST"])
    def login():
        """
        Log in a user.
        """
        try:
            login_data = UserLoginSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify({"error": "Validation error", "messages": err.messages}), 400

        user_service: UserService = app.user_service
        user = user_service.authenticate_user(login_data)
        if user:
            token = user.encode_auth_token(user.user_id)
            return jsonify({
                "message": "Logged in successfully",
                "token": token,
                "user_id": user.user_id,
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    @app.route("/user/logout", methods=["POST"])
    @require_auth
    def logout(user_id):
        """
        Log out the current user.
        ---
        tags:
          - Users
        responses:
          200:
            description: Successfully logged out
        """
        return jsonify({"message": "Logged out successfully"}), 200

    @app.route("/user/consent", methods=["PUT"])
    @require_auth
    @require_owner(lambda **kwargs: app.user_service.get_user(kwargs.get("user_id")))
    def update_consent(user_id):
        consent = request.json.get("consent")
        if consent is None:
            return jsonify({"error": "Consent value is required"}), 400

        user_service: UserService = app.user_service
        user = user_service.update_consent(user_id, consent)
        return jsonify(user_schema.dump(user)), 200