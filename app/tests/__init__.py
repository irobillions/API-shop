import json
import unittest

from faker import Faker

from app.authentication.infrastructure.services import BcryptHashingService
from app.authentication.models import User
from app.factory import create_app, db
from app.roles.models import Role


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.client = self.app.test_client
        self.db = db

        with self.app.app_context():
            self.db.create_all()

    def save_user(self, role):
        fake = Faker()
        hashing_service = BcryptHashingService()
        data = {
            'email': fake.email(),
            'username': fake.user_name(),
            'password': hashing_service.hash('password'),
            'last_name': 'John',
            'first_name': 'Doe',
            'roles': [role],
        }

        with self.app.app_context():
            self.db.session.add(User(**data))
            self.db.session.commit()

        return {
            'email': data['email'],
            'password': 'password',
        }

    def authenticate(self, role_name="ROLE_USER"):
        with self.app.app_context():
            role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
        path = ("seller", "client")[role_name != "ROLE_SELLER"]
        response = self.client().post(f"/users/login-{path}",
                                      data=json.dumps(self.save_user(role)),
                                      content_type="application/json")
        response_data = json.loads(response.data)
        if 'accessToken' not in response_data:
            raise Exception("Fails to authenticate user")
        return response_data['accessToken']
