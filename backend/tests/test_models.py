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
    results = patient.json()
    assert results['first_name'] == 'Testy'
    assert results['last_name'] == 'McPatient'
    assert results['gender'] == 'M'
