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
from mind_matter_api import commands
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
    logger = logging.getLogger(__name__)

    app.config.from_object(config_object)
    app.config["SQLALCHEMY_RECORD_QUERIES"] = True
    app.secret_key = os.environ.get("SECRET_KEY", "default-secret-key")
    app.config["SESSION_COOKIE_SECURE"] = True
    from mind_matter_api.models.users import User
    register_extensions(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_routes(app)
    print(f'app.url_map')
    configure_logger(app)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": app.config['CORS_ALLOWED_ORIGINS']}})
    logger.info(f"CORS enabled for {app.config['CORS_ALLOWED_ORIGINS']}")

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

    # with app.app_context():  # Activate the application context
    #     db.create_all()

    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok", "message": "API is running"}), 200

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
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Return JSON response for errors."""
        error_code = getattr(error, "code", 500)
        return jsonify(error=str(error), code=error_code), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    from mind_matter_api.models import User
    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.seed)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    if not app.logger.handlers:
        app.logger.addHandler(handler)