import pytest
import os

from backend_app.api.models import Patient


@pytest.fixture
def simple_xml(datadir):
    with open(os.path.join(datadir, 'simple.xml'), 'r') as xml_file:
        data = xml_file.read()
    return data


def test_parse_names(simple_xml):
    patient = Patient()
    patient.simple_xml = simple_xml
    patient.jurisdiction = "WA"
    results = patient.json()
    assert results['first_name'] == 'Testy'
    assert results['last_name'] == 'McPatient'
    assert results['gender'] == 'M'
    assert results['birthdate'] == '19990101'
    assert results['address'] == '123 Main Blvd'
    assert results['city'] == 'Renton'
    assert results['state'] == 'WA'
    assert results['zip'] == '98006-1234'
    assert results['phone'] == '206-123-4567'
    assert results['race'] == 'UNK'
    assert results['ethnicity'] == 'UNK'
    assert results['reportable_conditions'] == (
        'Disease caused by severe acute respiratory syndrome coronavirus 2 (disorder)')
    assert results['jurisdiction'] == 'WA'
    assert results['date_of_report'] == '20210719173828-0700'
    assert results['reason_for_report'] == (
        'Disease caused by severe acute respiratory syndrome coronavirus 2 (disorder)')
