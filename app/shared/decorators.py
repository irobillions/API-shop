from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims


def has_role(role):
    def role_required(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            if role not in claims['roles']:
                return jsonify({
                    'message': 'You are not allowed to access this endpoint',
                    'success': False
                }), 401
            else:
                return fn(*args, **kwargs)

        return wrapper

    return role_required
