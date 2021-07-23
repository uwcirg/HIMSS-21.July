from flask import Blueprint
from ..db import db
from .models import Patient

base_blueprint = Blueprint('base', __name__)


@base_blueprint.route('/')
def root():
    return {'ok': True}


@base_blueprint.route('/init-db')
def init_db():
    db.drop_all()
    db.create_all()
    return {'ok': True}


@base_blueprint.route('/dummy')
def dummy():
    p = Patient()
    p.simple_xml = "<xml><not>really</not></xml>"

    db.session.add(p)
    db.session.commit()
    return {'added': p}


@base_blueprint.route('/Patient')
def patient_list():
    patients = []
    for p in Patient.query():
        patients.append({
            'id': p.id,
            'xml': p.simple_xml
        })
    return {'patients': patients}
