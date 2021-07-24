from flask_sqlalchemy import SQLAlchemy
from ..db import db


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text, nullable=True)
    simple_xml = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return "<Patient %d>" % self.id
