from datetime import datetime

from app.factory import db


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(100), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=True)  # nullable because I have not implemented it

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', backref='addresses')

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_summary(self):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.street_address,
            'zip_code': self.zip_code,
            'city': self.city,
            'country': self.country,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

        return data
