import random

from app.factory import db
from datetime import datetime
from app.adresses.models import Address
from app.authentication.models import User

ORDER_STATUS = ['processed', 'delivered', 'in transit', 'shipped', 'canceled', 'processing']
PAIEMENT_METHOD = ['delivery_paeiment', 'card_paiement']
DELIVERY_MODE = ['STANDARD DELIVERY', 'EXPRESS DELIVERY', 'CUSTOM DELIVERY']


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_status = db.Column(db.Integer)
    tracking_number = db.Column(db.String(255))
    order_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    amount_TTC = db.Column(db.Integer, nullable=False)
    paiement_method = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    delivery_mode = db.Column(db.Integer, nullable=False)
    delivery_date_achieve = db.Column(db.DateTime, nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    address = db.relationship(Address, foreign_keys=[address_id], lazy=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', foreign_keys=[user_id], lazy=False)

    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    seller = db.relationship('User', foreign_keys=[seller_id], lazy=False)

    def get_summary(self, include_order_item=False):
        articles = {

            'id': self.id,
            'user_id': self.user_id,
            'order_status': ORDER_STATUS[self.order_status],
            'tracking_number': self.tracking_number,
            'address': self.address.get_summary(),
            'paiement_method': PAIEMENT_METHOD[int(self.paiement_method)],
            'order_date_do': self.order_date,
            'amout_TTC': self.amount_TTC,
            'delivery_mode': DELIVERY_MODE[int(self.delivery_mode)],
            'delivery_data_achieve': self.delivery_date_achieve
        }

        if include_order_item:
            articles['order_items'] = []
            for order_item in self.order_items:
                articles['order_items'].append(order_item.get_summary())

        else:
            articles['order_items_count'] = len(self.order_items)
        return articles

    def get_total_amount(self):
        self.amount_TTC = 0
        for order_item in self.order_items:
            self.amount_TTC += order_item.product.price * order_item.quantity

    def __repr__(self):
        return '<Order %r>' % self.tracking_number


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), index=True, unique=True)
    # slug = db.Column(db.String(255), index=True)
    # quality = db.Column(db.String(100), index=True)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())
    # constructor = db.Column(db.String, nullable=True)

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    order = db.relationship('Order', backref='order_items')

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref='order_items', lazy=False)

    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    # user = db.relationship('User', backref='products_bought')

    def get_summary(self):
        seller_item = User.query.filter(User.id == self.product.seller_id).first()
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'product_id': self.product_id,
            'product_seller_id': seller_item.username,
            'product_category': [c.name for c in self.product.categories],
            'price': self.price,
            'quantity': self.quantity
            # 'constructor': self.constructor,
        }

    def slug_generator_for_item(self, prdt_name, username):
        self.slug = 'order-0' + str(random.randint(0, 100)) + 'item-0' + str(random.randint(0, 100)) + '-' + str(
            username) + str(prdt_name)

    # verifier si la quantité commandé correspond au stock sinon la commande ne peut etre valide


"""
seller_orders = db.Table('seller_orders',
                         db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
                         db.Column('seller_id', db.Integer, db.ForeignKey('users.id')))

"""
