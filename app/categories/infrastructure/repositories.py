from app.categories.models import Category
from app.factory import db
from app.categories.domain.repositories import CategoryRepository


class FlaskCategoryRepository(CategoryRepository):
    def save(self, category):
        category_to_add = Category(name=category.name,
                                   description=category.description)
        db.session.add(category_to_add)
        db.session.commit()
        return Category.query.filter_by(name=category_to_add.name).first()

    def get_all(self):
        return Category.query.all()

    def get_in_list(self, items):
        return Category.query.filter(Category.id.in_(items)).all()
