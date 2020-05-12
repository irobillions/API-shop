from app.factory import db, bcrypt
from app.roles.models import users_roles
from datetime import datetime
# from app.orders.models import seller_orders


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(300), nullable=False)
    last_name = db.Column(db.String(300), nullable=False)

    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    roles = db.relationship('Role', secondary=users_roles, backref='users')
    # orders = db.relationship('Order', secondary=seller_orders, backref='sellers', lazy='dynamic') # trouver une
    # autre solution pour affecter les commandes au fournisseur specifique

    def __repr__(self):
        return f'<User {self.id} {self.username} {self.email} {self.first_name} {self.last_name}>'

    def is_admin(self):
        return 'ROLE_ADMIN' in [r.name for r in self.roles]

    def is_seller(self):
        return 'ROLE_SELLER' in [r.name for r in self.roles]

    def get_user_detail(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'role': [r.name for r in self.roles],
            'user_images': [i.images for i in self.images]
        }
