import jwt
import datetime
from flask import request , current_app

def create_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    access_token = jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')
    return access_token

def get_current_user_id():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    access_token = auth_header.split(' ', 1)[1]
    try:
        payload = jwt.decode(access_token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.InvalidTokenError:
        return None
   