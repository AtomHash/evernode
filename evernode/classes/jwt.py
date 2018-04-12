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
    data = None

    def __init__(self):
        self.app = current_app
        self.app_key = self.app.config['KEY']
        self.app_secret = self.app.config['SERECT']
        self.request = request

    def create_token(self, data, seconds_to_expire=180) -> str:
        """ Construct a JWT """
        jwt_token = jwt.encode({
            'data': data,
            'exp': datetime.utcnow() + timedelta(seconds=seconds_to_expire)},
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
                    self.data = jwt.decode(
                        decrypted_token,
                        self.app_secret)['data']
                    return True
                except (Exception, BaseException) as error:
                    """ catch all decoding exceptions """
                    if current_app.config['DEBUG']:
                        print(error)
                    return False
            else:
                return False
        return False
