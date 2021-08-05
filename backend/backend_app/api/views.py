from flask import Blueprint, abort, jsonify, make_response, redirect, render_template
from os import getenv

from ..db import db
from .models import Patient, RckmsConditionCodes

base_blueprint = Blueprint('base', __name__)


@base_blueprint.route('/')
def root():
    return redirect('/static/frontend/index.html')


@base_blueprint.route('/logout')
def logout():
    resp = make_response(render_template('logout.html'))
    resp.set_cookie('mod_auth_openidc_session', '', expires=0)
    return resp


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


@base_blueprint.route('/Patient/<int:patient_id>', methods=['DELETE'])
def patient_delete(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        abort(404)

    db.session.delete(patient)
    db.session.commit()

    return {'deleted patient: ': patient_id}


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


@base_blueprint.route('/REMOTE_USER')
def remote_user():
    return jsonify(REMOTE_USER=getenv('X-REMOTE-USER', None))


@base_blueprint.route('/api/settings')
def settings():
    # for now, just return the one(s) the front end needs
    return {'DELETE_CONTROLS': 'show'}
