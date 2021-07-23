from flask import Blueprint

base_blueprint = Blueprint('base', __name__)

@base_blueprint.route('/')
def root():
    return {'ok': True}


@base_blueprint.route('/init-db')
def init_db():
    from backend_app.db import db
    db.create_all()
    return {'ok': True}
