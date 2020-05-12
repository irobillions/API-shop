from app.factory import db
from datetime import datetime


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # user = relationship('User', backref=db.backref('comments'))
    user = db.relationship('User', foreign_keys=[user_id], lazy=False)

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    # product = relationship('Product', backref=db.backref('comments'))

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def get_summary(self, include_product=False, include_user=False):
        data = {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at,
        }

        if include_product:
            data['product'] = {
                'id': self.products.id,
                'name': self.products.name
            }

        if include_user:
            data['user'] = {
                'id': self.user_id,
                'username': self.user.username
            }
        return data
