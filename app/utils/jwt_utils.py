from flask_jwt_extended import create_access_token, get_jwt_identity

def create_token(user_id):
    return create_access_token(identity=user_id)

def get_current_user():
    return get_jwt_identity()