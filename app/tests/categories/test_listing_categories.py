from .. import AppTestCase
from app.authentication.infrastructure.services import BcryptHashingService
from app.roles.models import Role
from app.authentication.models import User
from app.categories.models import Category
import json
from faker import Faker
from app.categories.models import Category


class ListCategoriesTest(AppTestCase):
    def category_seeder(self):
        fake = Faker()
        return [
            Category(name=fake.name(), description=fake.sentence()),
            Category(name=fake.name(), description=fake.sentence()),
            Category(name=fake.name(), description=fake.sentence()),
            Category(name=fake.name(), description=fake.sentence()),
            Category(name=fake.name(), description=fake.sentence()),
        ]

    def test_list_categories_works_fine(self):
        categories = self.category_seeder()
        categories_name = list(map(lambda x: x.name, categories))
        with self.app.app_context():
            self.db.session.add_all(categories)
            self.db.session.commit()
        result = self.client().get("/categories/")
        self.assertEqual(200, result.status_code)
        json_result = json.loads(result.data)
        self.assertIn("items", json_result)
        self.assertEqual(5, len(json_result.get('items')))
        self.assertCountEqual(
            categories_name,
            list(map(lambda x: x.get('name'), json_result.get('items'))))
