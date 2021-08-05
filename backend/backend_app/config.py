"""Default configuration

Use env var to override
"""
import os

DELETE_CONTROLS = os.getenv("DELETE_CONTROLS", 'hide')
SERVER_NAME = os.getenv("SERVER_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")
# URL scheme to use outside of request context
PREFERRED_URL_SCHEME = os.getenv("PREFERRED_URL_SCHEME", 'http')
SQLALCHEMY_DATABASE_URI = os.getenv(
    "SQLALCHEMY_DATABASE_URI", "postgresql://mirthdb:mirthdb@db/mirthdb")
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Quiet warning
