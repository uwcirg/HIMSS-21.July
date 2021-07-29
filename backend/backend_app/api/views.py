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


@base_blueprint.route('/Patient')
def patient_list():
    patients = []
    for p in Patient.query.all():
        patients.append(p.json())
    return {'patients': patients}


@base_blueprint.route('/Patient/raw')
def patient_raw_list():
    patients = []
    for p in Patient.query.all():
        patients.append({
            'id': p.id,
            'uuid': p.uuid,
            'simple-xml': p.simple_xml,
            'jurisdiction': p.jurisdiction
        })
    return {'patients': patients}
