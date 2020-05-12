# all service we will implement for application but this is only interface and nothing else
# we must keep abstraction in the domain


class SessionService:
    def store(self, user):
        raise NotImplementedError

    def revoke(self):
        raise NotImplementedError

    def check_user_in_store(self):
        raise NotImplementedError

    def refresh(self, user):
        raise NotImplementedError

    def get_logged_user_identifier(self):
        raise NotImplementedError


class HashingService:
    def hash(self, to_hash):
        raise NotImplementedError

    def check(self, hashed, to_check):
        raise NotImplementedError
