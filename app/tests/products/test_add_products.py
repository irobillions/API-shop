from .. import AppTestCase
from app.products.models import Product
import uuid
from faker import Faker
from app.categories.models import Category
import json


class AddProductTest(AppTestCase):
    def product_data(self):
        fake = Faker()
        with self.app.app_context():
            self.db.session.add(Category(name=fake.name()))
            self.db.session.commit()

        return {
            "name": fake.name(),
            "description": fake.text(),
            "availability": fake.pybool(),
            "quality": fake.word(),
            "price": fake.pyfloat(min_value=20.00, max_value=10000.00),
            "stock": fake.pyint(),
            "manufacturer": fake.name(),
            "categories": [1]
        }

    def part_data_data(self):
        fake = Faker()
        return {
            "ref_part": fake.word(),
            "weight": fake.pyint(),
            "diameter": fake.pyint(),
            "dimension": fake.word(),
            "date_of_prod": fake.date_time().strftime("%Y-%m-%d %H:%M:%S"),
            "num_oem": str(uuid.uuid4()),
            "country_of_origin": fake.country(),
            "volume_of_part": fake.pyint()
        }

    def test_create_product_as_seller_works(self):
        access_token = self.authenticate("ROLE_SELLER")
        data = self.product_data()
        response = self.client().post(
            "/products/",
            headers=dict(Authorization=f"Bearer {access_token}"),
            data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(200, response.status_code)
        with self.app.app_context():
            self.assertEqual(1, Product.query.count())
            product = Product.query.get(1)
        self.assertIn("id", json.loads(response.data))
        for key in data:
            if key == 'categories':
                self.assertCountEqual(
                    data['categories'],
                    list(
                        map(lambda cat: cat.get('id'),
                            json.loads(response.data).get('categories'))))
            else:
                self.assertEqual(data.get(key),
                                 json.loads(response.data).get(key))

    def test_create_a_product_with_part_data_as_seller_works(self):
        access_token = self.authenticate("ROLE_SELLER")
        data = self.product_data()
        data['part_data'] = self.part_data_data()
        response = self.client().post(
            "/products/",
            headers=dict(Authorization=f"Bearer {access_token}"),
            data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(200, response.status_code)
        self.assertIn("part_data", json.loads(response.data))
        with self.app.app_context():
            self.assertEqual(1, Product.query.count())
            product = Product.query.get(1)
        self.assertIn("id", json.loads(response.data))
        for key in data:
            if key == 'categories':
                self.assertCountEqual(
                    data['categories'],
                    list(
                        map(lambda cat: cat.get('id'),
                            json.loads(response.data).get('categories'))))
            else:
                self.assertEqual(data.get(key),
                                 json.loads(response.data).get(key))
        for key in data['part_data']:
            self.assertEqual(
                data.get("part_data").get(key),
                json.loads(response.data).get("part_data").get(key))

    def test_send_a_product_with_non_valid_attributes_fails(self):
        access_token = self.authenticate("ROLE_SELLER")
        data = self.product_data()
        for key in data:
            data_copy = data.copy()
            data_copy.pop(key, None)
            response = self.client().post(
                "/products/",
                headers=dict(Authorization=f"Bearer {access_token}"),
                data=json.dumps(data_copy),
                content_type="application/json")
            self.assertEqual(422, response.status_code)
            self.assertIn(key, json.loads(response.data).get("message"))
            with self.app.app_context():
                self.assertEqual(0, Product.query.count())

    def test_sending_another_value_than_boolean_for_availability_fails(self):
        access_token = self.authenticate("ROLE_SELLER")
        data = self.product_data()
        data['availability'] = "false data"
        response = self.client().post(
            "/products/",
            headers=dict(Authorization=f"Bearer {access_token}"),
            data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(422, response.status_code)
        self.assertIn("availability", json.loads(response.data).get("message"))
        with self.app.app_context():
            self.assertEqual(0, Product.query.count())

    def test_sending_another_value_than_float_for_price_fails(self):
        access_token = self.authenticate("ROLE_SELLER")
        data = self.product_data()
        data['price'] = "false data"
        response = self.client().post(
            "/products/",
            headers=dict(Authorization=f"Bearer {access_token}"),
            data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(422, response.status_code)
        self.assertIn("price", json.loads(response.data).get("message"))
        with self.app.app_context():
            self.assertEqual(0, Product.query.count())

    def test_sending_another_value_than_int_for_stock_fails(self):
        access_token = self.authenticate("ROLE_SELLER")
        data = self.product_data()
        data['stock'] = "false data"
        response = self.client().post(
            "/products/",
            headers=dict(Authorization=f"Bearer {access_token}"),
            data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(422, response.status_code)
        self.assertIn("stock", json.loads(response.data).get("message"))
        with self.app.app_context():
            self.assertEqual(0, Product.query.count())

    def test_sending_empty_part_data_fails(self):
        access_token = self.authenticate("ROLE_SELLER")
        data = self.product_data()
        data['part_data'] = self.part_data_data()
        for key in data['part_data']:
            data_copy = data.copy()
            data_copy['part_data'] = data['part_data'].copy()
            del data_copy["part_data"][key]
            response = self.client().post(
                "/products/",
                headers=dict(Authorization=f"Bearer {access_token}"),
                data=json.dumps(data_copy),
                content_type="application/json")
            self.assertEqual(422, response.status_code)
            self.assertIn(key, json.loads(response.data).get("message"))
            with self.app.app_context():
                self.assertEqual(0, Product.query.count())
                product = Product.query.get(0)

    def test_weight_diameter_volume_of_part_as_other_value_than_int_should_fails(self):
        access_token = self.authenticate("ROLE_SELLER")
        data = self.product_data()
        data['part_data'] = self.part_data_data()
        for key in ('weight', 'diameter', 'volume_of_part'):
            data_copy = data.copy()
            data_copy['part_data'] = data['part_data'].copy()
            data_copy["part_data"][key] = "false data"
            response = self.client().post("/products/", headers=dict(Authorization=f"Bearer {access_token}"),
                                          data=json.dumps(data_copy),
                                          content_type="application/json")
            self.assertEqual(422, response.status_code)
            self.assertIn(key, json.loads(response.data).get("message"))
            with self.app.app_context():
                self.assertEqual(0, Product.query.count())
                product = Product.query.get(0)

    def test_date_of_prod_is_a_datetime(self):
        access_token = self.authenticate("ROLE_SELLER")
        data = self.product_data()
        data['part_data'] = self.part_data_data()
        data['part_data']['date_of_prod'] = "false data"
        response = self.client().post(
            "/products/",
            headers=dict(Authorization=f"Bearer {access_token}"),
            data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(422, response.status_code)
        self.assertIn("date_of_prod", json.loads(response.data).get("message"))
        with self.app.app_context():
            self.assertEqual(0, Product.query.count())
            product = Product.query.get(0)
