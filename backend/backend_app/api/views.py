from flask import Blueprint
from ..db import db
from .models import Patient, RckmsConditionCodes

base_blueprint = Blueprint('base', __name__)


@base_blueprint.route('/')
def root():
    return {'ok': True}


@base_blueprint.route('/init-db')
def init_db():
    from ..code_systems.load_table import load_rckms_condition_codes
    db.drop_all()
    db.create_all()
    load_rckms_condition_codes()
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


@base_blueprint.route('/RCKMS-codes')
def rckms_codes():
    codes = []
    for rcc in RckmsConditionCodes.query.all():
        codes.append({
            'id': rcc.id,
            'code': rcc.code,
            'code_system': rcc.code_system,
            'condition': rcc.condition
        })
    return {'RCKMS_ConditionCodes': codes}
