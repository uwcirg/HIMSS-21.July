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

    def first_name(self):
        xpath = "//n:patient/n:name/n:given/text()"
        return self._value_if_found(xpath)

    def last_name(self):
        xpath = "//n:patient/n:name/n:family/text()"
        return self._value_if_found(xpath)

    def gender(self):
        xpath = "//n:patient/n:administrativeGenderCode"
        return self._value_if_found(xpath, attribute='code')


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

        # Obtain list of methods from parser, all w/o leading '_',
        # by design return parsed value (or None if not found in XML).
        attributes = [
            method_name for method_name in dir(parser)
            if not method_name.startswith('_') and
            callable(getattr(parser, method_name))]
        for attr in attributes:
            results[attr] = getattr(parser, attr)()

        return results
