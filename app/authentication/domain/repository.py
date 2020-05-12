from app.authentication.domain.entities import User


# the user repository for communicate the domain with data but here we only put an interface because
# it must have an abstraction between data , the application shouldn't access directly to data it's like a contract
class UserRepository:

    def save(self, user):
        raise NotImplementedError

    def exists_with_email(self, email: str) -> bool:
        raise NotImplementedError

    def exists_with_username(self, username: str) -> bool:
        raise NotImplementedError

    def get_user_with_email_and_password(self, email: str, password: str) -> dict:
        raise NotImplementedError

    def get_user_by_email(self, email) -> User:
        raise NotImplementedError
