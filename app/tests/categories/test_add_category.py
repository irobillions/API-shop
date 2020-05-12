from .. import AppTestCase
import json
from app.categories.models import Category
from faker import Faker


class AddCategoryTest(AppTestCase):
    def test_create_category_with_name_as_seller_works(self):
        access_token = self.authenticate("ROLE_SELLER")
        response = self.client().post(
            "/categories/",
            headers=dict(Authorization=f"Bearer {access_token}"),
            data=json.dumps({"name": "Voitures"}),
            content_type="application/json")
        self.assertEqual(200, response.status_code)
        with self.app.app_context():
            self.assertEqual(1, Category.query.count())
            category = Category.query.get(1)
        self.assertEqual("Voitures", category.name)
        self.assertIn("id", json.loads(response.data))
        self.assertIn("name", json.loads(response.data))
        self.assertEqual("Voitures", json.loads(response.data)['name'])

    def test_create_category_without_name_as_seller_doesnt_work(self):
        access_token = self.authenticate("ROLE_SELLER")
        response = self.client().post(
            "/categories/",
            headers=dict(Authorization=f"Bearer {access_token}"),
            data=json.dumps({}),
            content_type="application/json")
        self.assertEqual(422, response.status_code)
        with self.app.app_context():
            self.assertEqual(0, Category.query.count())
        self.assertIn("name", json.loads(response.data).get('message'))

    def test_create_category_as_a_guest_doesnt_work(self):
        response = self.client().post("/categories/",
                                      data=json.dumps({'name': "Voitures"}),
                                      content_type="application/json")
        self.assertEqual(401, response.status_code)
        with self.app.app_context():
            self.assertEqual(0, Category.query.count())

    def test_create_category_as_a_simple_user_doesnt_work(self):
        access_token = self.authenticate()
        response = self.client().post(
            "/categories/",
            headers=dict(Authorization=f"Bearer {access_token}"),
            data=json.dumps({"name": "Voitures"}),
            content_type="application/json")
        self.assertEqual(401, response.status_code)
        with self.app.app_context():
            self.assertEqual(0, Category.query.count())
