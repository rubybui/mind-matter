# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
SECRET_KEY = env.str("SECRET_KEY")
SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT")

# Mail settings
MAIL_SERVER = env.str("MAIL_SERVER", default="smtp.gmail.com")
MAIL_PORT = env.int("MAIL_PORT", default=587)
MAIL_USE_TLS = env.bool("MAIL_USE_TLS", default=True)
MAIL_USERNAME = env.str("MAIL_USERNAME", default="")
MAIL_PASSWORD = env.str("MAIL_PASSWORD", default="")
MAIL_DEFAULT_SENDER = env.str("MAIL_DEFAULT_SENDER", default="")
MAIL_MAX_EMAILS = env.int("MAIL_MAX_EMAILS", default=None)
MAIL_ASCII_ATTACHMENTS = env.bool("MAIL_ASCII_ATTACHMENTS", default=False)
MAIL_SUPPRESS_SEND = env.bool("MAIL_SUPPRESS_SEND", default=False)

DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = (
    "flask_caching.backends.SimpleCache"  # Can be "MemcachedCache", "RedisCache", etc.
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
