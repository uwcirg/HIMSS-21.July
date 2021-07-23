from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from backend.backend_app.db import db
from backend.backend_app import api


def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask('backend_app')
    app.config.from_object('backend_app.config')
    app.config['TESTING'] = testing
    db.init_app(app)

    register_blueprints(app)
    configure_proxy(app)

    return app


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(api.views.base_blueprint)


def configure_proxy(app):
    """Add werkzeug fixer to detect headers applied by upstream reverse proxy"""
    if app.config.get('PREFERRED_URL_SCHEME', '').lower() == 'https':
        app.wsgi_app = ProxyFix(
            app=app.wsgi_app,

            # trust X-Forwarded-Host
            x_host=1,

            # trust X-Forwarded-Port
            x_port=1,
        )
