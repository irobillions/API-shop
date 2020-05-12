import json

from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_claims, get_jwt_identity

from app.authentication.domain.use_cases import RegisterUser, LogInUser, LogInUserSeller, GetUserInfo, \
    LogoutUser, ReauthenticateUser
from app.authentication.infrastructure.repositories import FlaskUserRepository
from app.authentication.infrastructure.services import TokenSessionService, BcryptHashingService, \
    UserEncoder
from app.authentication.shared.auth_request import RegisterUserRequest, LogInUserRequest, GetInfosUserRequest, \
    LogoutUserRequest, ReauthenticateUserRequest
import app.shared.response as res

# this represent the application part
from app.shared.serializers import STATUS_CODE

users = Blueprint('users', __name__, url_prefix='/users')


# the register route
@users.route('/register', methods=['POST'])
def register():
    register_use_case = RegisterUser(
        FlaskUserRepository(BcryptHashingService()), TokenSessionService())
    result = register_use_case(
        RegisterUserRequest.build_from_dict(request.json))
    return Response(json.dumps(result.value),
                    mimetype="application/json",
                    status=201)


@users.route('/login-client', methods=['POST'])
def login_client():
    login_use_case = LogInUser(FlaskUserRepository(BcryptHashingService()),
                               TokenSessionService())
    result = login_use_case(LogInUserRequest.build_from_dict(request.json))
    return Response(json.dumps(result.value),
                    mimetype="application/json",
                    status=STATUS_CODE[result.type])


@users.route('/login-seller', methods=['POST'])
def login_seller():
    login_use_case = LogInUserSeller(
        FlaskUserRepository(BcryptHashingService()), TokenSessionService())
    result = login_use_case(LogInUserRequest.build_from_dict(request.json))
    return Response(json.dumps(result.value),
                    mimetype="application/json",
                    status=STATUS_CODE[result.type])


@users.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh_user_token():
    reauthenticate_use_case = ReauthenticateUser(
        FlaskUserRepository(BcryptHashingService()), TokenSessionService())
    result = reauthenticate_use_case(
        ReauthenticateUserRequest.build_from_dict({
            "user":
                reauthenticate_use_case.user_repo.get_user_by_id(
                    get_jwt_identity())
        }))
    return Response(json.dumps(result.value),
                    mimetype="application/json",
                    status=STATUS_CODE[result.type])


@users.route('/auth/info', methods=['GET'])
@jwt_required
def get_user_infos():
    claims = get_jwt_claims()
    get_infos_use_case = GetUserInfo(
        FlaskUserRepository(BcryptHashingService()))
    result = get_infos_use_case(GetInfosUserRequest.build_from_dict(claims))
    return Response(json.dumps(result.value, cls=UserEncoder),
                    mimetype="application/json",
                    status=STATUS_CODE[result.type])


@users.route('/logout', methods=['POST'])
@jwt_refresh_token_required
def logout():
    logout_use_case = LogoutUser(TokenSessionService())
    result = logout_use_case(LogoutUserRequest())
    return Response(json.dumps(result.value),
                    mimetype="application/json",
                    status=202)


@users.route("/")
def testing():
    return "Hello World"
