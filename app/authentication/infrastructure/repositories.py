from app.authentication.domain.repository import UserRepository
from app.factory import db
from ..models import User
from app.roles.models import Role


# here the repository which communicate with database in the infrastructure
# the real implementation of repository
class FlaskUserRepository(UserRepository):
    def __init__(self, hashing_service):
        self.hashing_service = hashing_service

    def save(self, user):
        role = Role.query.filter(Role.name == user.roles).first()
        user_to_add = User(username=user.username,
                           first_name=user.first_name,
                           last_name=user.last_name,
                           email=user.email,
                           password=self.hashing_service.hash(user.password),
                           roles=[role])
        db.session.add(user_to_add)
        db.session.commit()
        return User.query.filter_by(username=user_to_add.username).first()

    def exists_with_email(self, email: str) -> bool:
        return User.query.filter_by(email=email).first() is not None

    def exists_with_username(self, username: str) -> bool:
        return User.query.filter_by(username=username).first() is not None

    def get_user_with_email_and_password(self, email: str,
                                         password: str) -> dict:
        user = User.query.filter_by(email=email).first()
        if user:
            if self.hashing_service.check(user.password, str(password)):
                return {'user': user, 'attr': None}
            return {'user': None, 'attr': 'password'}
        return {'user': None, 'attr': 'email'}

    def get_user_by_email(self, email) -> User:
        return User.query.filter_by(email=email).first()

    # this function has no relation with domain because in the domain the entity does not id
    def get_user_by_id(self, _id):
        return User.query.get(_id)
