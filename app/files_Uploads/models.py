from app.factory import db
from datetime import datetime


class FileUpload(db.Model):
    __tablename__ = 'file_uploads'

    id = db.Column('id', db.Integer, primary_key=True)
    type = db.Column('type', db.String(15))  # this will be our discriminator

    file_path = db.Column(db.String(300), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    original_name = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'FileUpload'
    }


class ProductImage(FileUpload):
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    product = db.relationship('Product', backref='images')

    __mapper_args__ = {
        'polymorphic_identity': 'ProductImage'
    }


class CategoryImage(FileUpload):
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship('Category', backref='images')

    __mapper_args__ = {
        'polymorphic_identity': 'CategoryImage'
    }


class UserImage(FileUpload):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', backref='images')

    __mapper_args__ = {
        'polymorphic_identity': 'UserImage'
    }


class CarBrandImage(FileUpload):
    carbrand_id = db.Column(db.Integer, db.ForeignKey('carbrands.id'), nullable=True)
    carbrand = db.relationship('CarBrand', backref='images')

    __mapper_args__ = {
        'polymorphic_identity': 'CarBrandImage'
    }


class CarModelImage(FileUpload):
    carmodel_id = db.Column(db.Integer, db.ForeignKey('carmodels.id'), nullable=True)
    carmodel = db.relationship('CarModel', backref='images')

    __mapper_args__ = {
        'polymorphic_identity': 'CarModelImage'}


class QuoteFileUploaded(FileUpload):
    quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id'), nullable=True)
    quote = db.relationship('Quote', backref='files')

    __mapper_args__ = {
        'polymorphic_identity': 'QuoteFile'}
