# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys
import os
from environs import Env

from flask import Flask, jsonify
from flasgger import Swagger
from flask_cors import CORS

from mind_matter_api.models import User
from mind_matter_api.api import register_routes

from mind_matter_api.schemas import UserSchema, UserBodySchema
from mind_matter_api.extensions import (
    cache,
    csrf_protect,
    db,
    ma,
    debug_toolbar,
    flask_static_digest,
    migrate,
    login_manager,
)


def create_app(config_object="mind_matter_api.settings"):
    """Create application factory.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__, root_path=os.path.dirname(os.path.abspath(__file__)))
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # <--- THIS LINE

    logger = logging.getLogger(__name__)

    # Load configuration
    app.config.from_object(config_object)
    app.config["SQLALCHEMY_RECORD_QUERIES"] = True
    app.secret_key = os.environ.get("SECRET_KEY", "default-secret-key")
    app.config["SESSION_COOKIE_SECURE"] = True

    # Initialize extensions
    register_extensions(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_routes(app)
    configure_logger(app)


    # Swagger UI
    Swagger(
        app,
        template={
            "swagger": "2.0",
            "info": {
                "title": "Mind Matter API",
                "description": "API for managing users",
                "version": "1.0.0",
            },
            "definitions": {
                "UserSchema": UserSchema().dump({}),
                "UserBodySchema": UserBodySchema().dump({}),
            },
            "paths": {},
        },
    )

    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok", "message": "API is running"}), 200

    # Conditionally register CLI commands (exclude in production runtime)
    register_commands(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    cache.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    # csrf_protect.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    login_manager.init_app(app)


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        error_code = getattr(error, "code", 500)
        return jsonify(error=str(error), code=error_code), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        return {"db": db, "User": User}
    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands except in production runtime."""
    # Only add test, lint, seed commands when not in production environment
    env = app.config.get("ENV", os.environ.get("FLASK_ENV", "production"))
    if env != 'production':
        from mind_matter_api import commands
        app.cli.add_command(commands.test)
        app.cli.add_command(commands.lint)
        app.cli.add_command(commands.seed)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    if not app.logger.handlers:
        app.logger.addHandler(handler)
