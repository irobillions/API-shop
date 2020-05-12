import random

from pyparsing import unicode
from slugify import slugify

from app.factory import db
from datetime import datetime
from sqlalchemy import event

from app.shared.serializers import randomString


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(255), index=True, unique=True)
    description = db.Column(db.String(300))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow(), index=True)
    updated_at = db.Column(db.DateTime())

    def get_summary(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_urls': [image.file_path.replace('\\', '/') for image in self.images]
        }

    def __repr__(self):
        return self.name

    def slug_generator_for_category(self, name):
        self.slug = 'catg-0'+str(random.randint(0, 100))+str(randomString(6))+'-'+str(name)

"""
@event.listens_for(Category.name, 'set')
def receive_set(target, value, oldvalue, initiator):
    target.slug = slugify(unicode(value))
"""

products_categories = \
    db.Table("products_categories",
             db.Column("category_id", db.Integer, db.ForeignKey("categories.id")),
             db.Column("product_id", db.Integer, db.ForeignKey("products.id")))
