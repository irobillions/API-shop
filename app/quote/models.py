import random

from app.factory import db
from datetime import datetime

from app.shared.serializers import randomString


class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    quote_title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), index=True, unique=True)
    content = db.Column(db.Text, nullable=False)
    carModel_information = db.Column(db.String(255), nullable=True)
    immatricuation = db.Column(db.String(255), nullable=True)
    num_chassis = db.Column(db.String(255), nullable=False)
    num_vin = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], lazy=False)

    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def get_summary(self, include_file=False):
        quote_summary = {
            'title': self.quote_title,
            'content': self.content,
            'carmodel_inf': self.carModel_information,
            'immatriculation': self.immatricuation,
            'num_chassis': self.num_chassis,
            'num_vin': self.num_vin,
            'created_at': self.created_at
        }
        if include_file:
            quote_summary['files'] = [i.file_path for i in self.files]

        return quote_summary

    def slug_generator_for_quote(self, username):
        self.slug = 'quote-0' + str(random.randint(0, 100)) + str(randomString(5)) + '-' + str(username)
