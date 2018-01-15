"""
    Easy JSON Web Token implementation for Flask
"""
import re
import jwt
from datetime import datetime, timedelta
from flask import current_app, Flask, request
from .security import Security


class JWT:
    """ Gets request information to validate JWT """
    token = None
    app = Flask
    app_key = None
    app_secret = None
    request = None
    session_id = None

    def __init__(self):
        self.app = current_app
        self.app_key = self.app.config['KEY']
        self.app_secret = self.app.config['SERECT']
        self.request = request

    def create_token(self, session_id, days_to_expire=7) -> str:
        """ Construct a JWT """
        jwt_token = jwt.encode({
            'data': {
                'session_id': session_id
            },
            'exp': datetime.utcnow() + timedelta(days=days_to_expire)},
            self.app_secret)
        return Security.encrypt(jwt_token)

    def verify_token(self) -> bool:
        """ Use request information to validate JWT """
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            parsed_token = re.search('Bearer (.+)', token)
            if parsed_token:
                jwt_token = parsed_token.group(1)
                try:
                    decrypted_token = Security.decrypt(jwt_token)
                    session_id = \
                        jwt.decode(
                            decrypted_token,
                            self.app_secret)['data']['session_id']
                    self.session_id = session_id
                    return True
                except (Exception, BaseException) as error:
                    """ catch all decoding exceptions """
                    if current_app.config['DEBUG']:
                        print(error)
                    return False
            else:
                return False
        return False
