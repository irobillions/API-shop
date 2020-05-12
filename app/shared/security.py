from app.factory import jwt
from app.authentication.models import User


# Using the user_claims_loader, we can specify a method that will be
# called when creating access tokens, and add these claims to the said
# token. This method is passed the identity of who the token is being
# created for, and must return data that is json serializable
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.filter(User.id == identity).first()
    return {
        'user_id': user.id,
        'email': user.email,
        'roles': [role.name for role in user.roles]
    }


# to charge an user as current user when authenticating
@jwt.user_loader_callback_loader
def user_loader(user_id):
    # the user will be now available in current_user
    return User.query.get(user_id)


def validate_file_upload(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['png', 'jpeg', 'jpg']
