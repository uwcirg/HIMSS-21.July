from lxml import etree
from ..db import db


class SimpleParser(object):
    def __init__(self, xml):
        self.namespaces = {'n': 'urn:hl7-org:v3'}
        self.tree = etree.fromstring(xml)

    def first_name(self):
        found = self.tree.xpath(
            "//n:patient/n:name/n:given/text()",
            namespaces=self.namespaces)
        if found:
            return found[0]

    def last_name(self):
        found = self.tree.xpath(
            "//n:patient/n:name/n:family/text()",
            namespaces=self.namespaces)
        if found:
            return found[0]

    def gender(self):
        found = self.tree.xpath(
            "//n:patient/n:administrativeGenderCode/n:code/text()",
            namespaces=self.namespaces)
        if found:
            return found[0]


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text, nullable=True)
    simple_xml = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return "<Patient %d>" % self.id

    def json(self):
        """Return dict of attributes from XML if found"""
        results = {'id': self.id, 'uuid': self.uuid}
        if not self.simple_xml:
            return results
        parser = SimpleParser(self.simple_xml)
        results['first_name'] = parser.first_name()
        results['last_name'] = parser.last_name()
        results['gender'] = parser.gender()

        return results
