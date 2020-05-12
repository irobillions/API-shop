import app.shared.response as res
from app.authentication.domain.entities import User
from app.shared.use_case import UseCase


# this is all authentication use case we put it in the domain because it is pure python code
# and do not communicate with database directly et do not depend from another module
# for each use case we use a request which is sent from the client side and we process it
class RegisterUser(UseCase):
    def __init__(self, user_repo, session_service):
        self.user_repo = user_repo
        self.session_service = session_service

    def process_request(self, request):
        if self.user_repo.exists_with_email(request.email):
            return res.ResponseFailure.build_from_error_dict(
                {'email': 'the email already exists in the database'})
        if self.user_repo.exists_with_username(request.username):
            return res.ResponseFailure.build_from_error_dict(
                {'username': 'your username already exist in the database'})

        user = User.from_dict(request.attributes)
        user_registered = self.user_repo.save(user)
        result = self.session_service.store(user_registered)
        return res.ResponseSuccess(result)


class LogInUser(UseCase):
    def __init__(self, user_repo, session_service):
        self.user_repo = user_repo
        self.session_service = session_service

    def process_request(self, request):
        user = self.user_repo.get_user_with_email_and_password(
            request.email, request.password)

        if user['user'] is None:
            return res.ResponseFailure.build_from_error_dict({
                f"{user['attr']}":
                    "your credentials does not match our records"
            })
        if 'ROLE_USER' not in [r.name for r in user['user'].roles]:
            return res.ResponseFailure.build_from_error_dict(
                {"role": "unauthorized"})
        result = self.session_service.store(user['user'])
        return res.ResponseSuccess(result)


class LogInUserSeller(UseCase):
    def __init__(self, user_repo, session_service):
        self.user_repo = user_repo
        self.session_service = session_service

    def process_request(self, request):
        user = self.user_repo.get_user_with_email_and_password(
            request.email, str(request.password))
        if user['user'] is None:
            return res.ResponseFailure.build_from_error_dict({
                f"{user['attr']}":
                    "your credentials does not match our records"
            })

        if 'ROLE_SELLER' not in [r.name for r in user['user'].roles]:
            return res.ResponseFailure.build_from_error_dict(
                {"role": "unauthorized"})
        result = self.session_service.store(user['user'])
        return res.ResponseSuccess(result)


# reauthenticate user if the access token expires and use the refresh token for that
class ReauthenticateUser(UseCase):
    def __init__(self, user_repo, session_service):
        self.user_repo = user_repo
        self.session_service = session_service

    def process_request(self, request):
        result = self.session_service.refresh(request.user)
        return res.ResponseSuccess(result)


# revoke access token to logout
class LogoutUser(UseCase):
    def __init__(self, session_service):
        self.session_service = session_service

    def process_request(self, request):
        if not self.session_service.check_user_in_store():
            return res.ResponseFailure.build_from_error_dict(
                {"message": "you are not logged in"})
        self.session_service.revoke()
        return res.ResponseSuccess(
            {"message": "you have been logout successfully"})


# get user infos
class GetUserInfo(UseCase):
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def process_request(self, request):
        user = self.user_repo.get_user_by_email(request.email)
        if not user:
            return res.ResponseFailure.build_from_error_dict(
                {"email": "email does not match"})

        return res.ResponseSuccess(user)
