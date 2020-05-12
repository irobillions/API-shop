import json

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, \
    verify_jwt_refresh_token_in_request, get_raw_jwt, get_jwt_claims

from app.authentication.domain.services import SessionService, HashingService
from app.factory import bcrypt, jwt
import app.shared.security
import datetime

from ..models import User


# implementation all services
class TokenSessionService(SessionService):
    blacklist = set()

    def store(self, user):
        access_token = create_access_token(
            identity=user.id,
            fresh=True,
            expires_delta=datetime.timedelta(seconds=3))
        refresh_token = create_refresh_token(identity=user.id)
        return {
            'success': True,
            'accessToken': access_token,
            'refreshToken': refresh_token,
            # 'role': [r.name for r in user.roles]
        }

    def refresh(self, user):
        verify_jwt_refresh_token_in_request()
        access_token = create_access_token(
            identity=user.id,
            fresh=False,
            expires_delta=datetime.timedelta(minutes=3600))

        return {
            'success': True,
            'accessToken': access_token,
        }

    def get_logged_user_identifier(self):
        claims = get_jwt_claims()
        return claims['email']

    def check_user_in_store(self):
        return get_jwt_identity() is not None

    def revoke(self):
        jti = get_raw_jwt()['jti']
        TokenSessionService.blacklist.add(jti)

    @staticmethod
    @jwt.token_in_blacklist_loader
    def _check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in TokenSessionService.blacklist


# to crypt user password
class BcryptHashingService(HashingService):
    def hash(self, to_hash):
        return bcrypt.generate_password_hash(to_hash).decode('utf-8')

    def check(self, hashed, to_check):
        return bcrypt.check_password_hash(hashed, to_check)


# user encoder to transform python object in json
class UserEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, User):
            return {
                'email': o.email,
                'username': o.username,
                'roles': [r.name for r in o.roles],
                'lastName': o.last_name,
                'firstName': o.first_name
            }
        return json.JSONEncoder.default(self, o)
