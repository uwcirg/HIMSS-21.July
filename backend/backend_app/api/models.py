from flask_sqlalchemy import SQLAlchemy
from ..db import db


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    simple_xml = db.Column(db.Text, nullable=True)
    eicr_html = db.Column(db.Text, nullable=True)
    rr_html = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return "<Patient %d>" % self.id
