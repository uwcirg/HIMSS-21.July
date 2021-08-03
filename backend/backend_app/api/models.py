from flask import has_app_context
from lxml import etree
from ..db import db


class SimpleParser(object):
    """Specialized XPath parser for SimpleXML from Mirth Channel

    NB - client code expects every method not starting with '_' will
    return the respective value (if found).

    """
    def __init__(self, xml):
        self.namespaces = {'n': 'urn:hl7-org:v3'}
        self.tree = etree.fromstring(xml)

    def _value_if_found(self, xpath, attribute=None):
        found = self.tree.xpath(xpath, namespaces=self.namespaces)
        if found:
            if attribute:
                return found[0].get(attribute)
            return found[0]

    def _child_items(self, xpath):
        results = {}
        node = self.tree.xpath(xpath, namespaces=self.namespaces)
        if not node:
            return

        for child in node[0]:
            # strip namespace from tag
            tag = child.tag
            close_namespace_index = tag.find('}')
            tag = tag[close_namespace_index+1:]
            results[tag] = child.text
        return results or None

    def address(self):
        xpath = "//n:patient/n:address/n:streetAddressLine/text()"
        return self._value_if_found(xpath)

    def city(self):
        xpath = "//n:patient/n:address/n:city/text()"
        return self._value_if_found(xpath)

    def state(self):
        xpath = "//n:patient/n:address/n:state/text()"
        return self._value_if_found(xpath)

    def zip(self):
        xpath = "//n:patient/n:address/n:postalCode/text()"
        return self._value_if_found(xpath)

    def telecom(self):
        xpath = "//n:patient/n:telecommunications/n:telecom"
        return self._child_items(xpath)

    def raceCode(self):
        xpath = "//n:patient/n:raceCode"
        return self._child_items(xpath)

    def ethnicGroupCode(self):
        xpath = "//n:patient/n:ethnicGroupCode"
        return self._child_items(xpath)

    def birthdate(self):
        xpath = "//n:patient/n:dateOfBirth/text()"
        return self._value_if_found(xpath)

    def first_name(self):
        xpath = "//n:patient/n:name/n:given/text()"
        return self._value_if_found(xpath)

    def last_name(self):
        xpath = "//n:patient/n:name/n:family/text()"
        return self._value_if_found(xpath)

    def gender(self):
        xpath = "//n:patient/n:administrativeGenderCode/n:code/text()"
        return self._value_if_found(xpath)

    def reportable_condition(self):
        code = self._value_if_found("//n:rr/n:condition/n:code/text()")
        code_system = self._value_if_found("//n:rr/n:condition/n:codeSystem/text()")
        if code and code_system and has_app_context():
            found = RckmsConditionCodes.query.filter(
                RckmsConditionCodes.code == code).filter(
                RckmsConditionCodes.code_system == code_system).first()
            if found:
                return found.condition

        return self._value_if_found('//n:rr/n:condition/n:displayName/text()')

    def reason_for_report(self):
        xpath = "//n:rr/n:condition/n:displayName/text()"
        return self._value_if_found(xpath)

    def doc_id(self):
        xpath = "//n:docID/n:root/text()"
        return self._value_if_found(xpath)

    def date_of_report(self):
        xpath = "//n:effectiveTime/n:value/text()"
        return self._value_if_found(xpath)

    def provider(self):
        fname = self._value_if_found(
            "//n:encompassingEncounter/n:provider/n:name/n:given/text()")
        lname = self._value_if_found(
            "//n:encompassingEncounter/n:provider/n:name/n:family/text()")
        if lname and not lname.startswith('null'):
            return ', '.join((lname, fname))


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text, nullable=True)
    simple_xml = db.Column(db.Text, nullable=True)
    jurisdiction = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return "<Patient %d>" % self.id

    def json(self):
        """Return dict of attributes from XML if found"""
        results = {'id': self.id, 'uuid': self.uuid}
        if not self.simple_xml:
            return results
        parser = SimpleParser(self.simple_xml)

        # Obtain list of methods from parser, all w/o leading '_',
        # by design return parsed value (or None if not found in XML).
        attributes = [
            method_name for method_name in dir(parser)
            if not method_name.startswith('_') and
            callable(getattr(parser, method_name))]
        for attr in attributes:
            results[attr] = getattr(parser, attr)()

        results['jurisdiction'] = self.jurisdiction
        return results


class RckmsConditionCodes(db.Model):
    __tablename__ = 'rckms_condition_codes'
    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.Text, nullable=True)
    code = db.Column(db.Text, nullable=True)
    code_system = db.Column(db.Text, nullable=True)

    def from_parser(self):
        pass
