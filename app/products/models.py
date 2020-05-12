import random
from encodings.utf_8 import decode

from pyparsing import unicode
from slugify import slugify

from app.comments.serializer import CommentDetailsSerializer
from app.factory import db
from datetime import datetime
from sqlalchemy import event
from app.categories.models import products_categories
from app.comments.models import Comment
from app.car.models import CarModel
from app.shared.serializers import randomString

STATUS = ['Epuisé', 'En Stock', 'En arrivage']


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), index=True, unique=True)
    description = db.Column(db.Text, nullable=False)
    availability = db.Column(db.Boolean)
    quality = db.Column(db.String(100))
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    # promotion_rate = db.Column(db.Integer, nullable=True) // a voir plus tard
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    publish_on = db.Column(db.DateTime(), index=True, default=datetime.utcnow)

    categories = db.relationship('Category', secondary=products_categories, backref='products')

    comments = db.relationship('Comment', backref='products', lazy=False)

    partdata = db.relationship('PartData', uselist=False)

    def __repr__(self):
        return '<Product %r>' % self.name

    def __str__(self):
        return '<Product {}>'.format(self.name)

    def get_summary(self):
        products_infos = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock,
            'slug': self.slug,
            'availability': STATUS[self.availability],
            'rating': self.rating,
            'quality': self.quality,
            'marque': self.manufacturer,
            'comments_count': len(self.comments),
            'comments': [CommentDetailsSerializer(c, include_user=True).data for c in self.comments],
            'categories': [c.name for c in self.categories],
            'image_urls': [i.file_path for i in self.images]
        }

        if self.partdata is not None:
            products_infos['ref_part'] = self.partdata.ref_part,
            products_infos['weight'] = self.partdata.weight,
            products_infos['date_of_prod'] = self.partdata.date_of_prod,
            products_infos['num_oem'] = self.partdata.num_oem,
            products_infos['country_of_origin'] = self.partdata.country_of_origin,
            products_infos['volume_of_part'] = self.partdata.volume_of_part,
            products_infos['manufacturer'] = self.partdata.manufacturer
            products_infos['dimension'] = self.partdata.dimension
            products_infos['list_car_compt'] = [car.designation for car in self.partdata.car_compatibilities]

        return products_infos

    def slug_generator_for_product(self, seller_id, prd_name):
        self.slug = 'product-0' + str(random.randint(0, 100)) + '-' + 'sllr-0' + str(seller_id) + '-' + str(
            randomString(3)) + str(prd_name)


class PartData(db.Model):
    __tablename__ = 'partdatas'

    id = db.Column(db.Integer, primary_key=True)
    ref_part = db.Column(db.String(255), nullable=False, unique=True, index=True)
    weight = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=True)
    dimension = db.Column(db.String(100), nullable=True)
    date_of_prod = db.Column(db.DateTime(), nullable=True)
    num_oem = db.Column(db.String(300), nullable=False, unique=True, index=True)
    country_of_origin = db.Column(db.String(80), nullable=False)
    volume_of_part = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)

    car_compatibilities = db.relationship(CarModel, secondary='car_part_compts', backref='partdatas', lazy=False)

    car_compt = db.Table('car_part_compts',
                         db.Column('partdata_id', db.Integer, db.ForeignKey('partdatas.id')),
                         db.Column('carmodel_id', db.Integer, db.ForeignKey('carmodels.id')))


"""
@event.listens_for(Product.name, 'set')
def receive_set(target, value, oldvalue, initiator):
    print(type(value))
    target.slug = slugify(unicode(value)) # essayer value.decode('utf-8)
    target.slug = oldvalue.replace('target.name', 'value', 1) ## a tester 
"""
