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
    assert len(results['telecom']) == 3
    assert set(i['value'] for i in results['telecom']) == set(
        ('tel:+1-206-123-4567', 'fax:+1-206-123-6789', 'email:example@who.com'))
    assert results['raceCode']['code'] == '2054-5'
    assert results['raceCode']['displayName'] == 'Black or African American'
    assert results['ethnicGroupCode']['code'] == '2186-5'
    assert results['ethnicGroupCode']['displayName'] == 'Not Hispanic or Latino'
    assert results['reportable_condition'] == (
        'Disease caused by severe acute respiratory syndrome coronavirus 2 (disorder)')
    assert results['jurisdiction'] == 'WA'
    assert results['date_of_report'] == '20210719173828-0700'
    assert results['reason_for_report'] == (
        'Disease caused by severe acute respiratory syndrome coronavirus 2 (disorder)')
    assert results['docID']['root'] == '1.2.840.114350.1.13.296.3.7.8.688883.176734'
    assert results['provider'] == 'Johnson, Jane'
    assert results['providerID']['root'] == '2.16.840.1.113883.4.6'
    assert results['healthcareOrganization']['name'] == 'YOUR REGIONAL MEDICAL CENTER'
    assert results['healthcareFacility']['address']['streetAddressLine'] == '123 MAIN BLVD'
