"""
    Easy JSON Web Token implementation for Flask
"""
import re
import jwt
from datetime import datetime, timedelta
from flask import current_app, request
from .security import Security


class JWT:
    """ Gets request information to validate JWT """
    token = None
    app_key = None
    app_secret = None
    request = None
    data = None
    errors = []

    def __init__(self):
        self.token = None
        self.data = None
        self.errors = []
        self.app_key = current_app.config['KEY']
        self.app_secret = current_app.config['SECRET']
        self.request = request

    def get_http_token(self):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            parsed_token = re.search('Bearer (.+)', token)
            if parsed_token:
                return parsed_token.group(1)
            else:
                return None
        return None

    def create_token(self, data, token_valid_for=180) -> str:
        """ Create encrypted JWT """
        jwt_token = jwt.encode({
            'data': data,
            'exp': datetime.utcnow() + timedelta(seconds=token_valid_for)},
            self.app_secret, algorithm="HS256")
        return Security.encrypt(jwt_token)

    def verify_token(self, token) -> bool:
        """ Verify encrypted JWT """
        try:
            self.data = jwt.decode(Security.decrypt(token), self.app_secret,
                                   algorithms=["HS256"])
            return True
        except (Exception, BaseException) as error:
            self.errors.append(error)
            return False
        return False

    def verify_http_auth_token(self) -> bool:
        """ Use request information to validate JWT """
        authorization_token = self.get_http_token()
        if authorization_token is not None:
            if self.verify_token(authorization_token):
                if self.data is not None:
                    self.data = self.data['data']
                    return True
                return False
            else:
                return False
        return False

    def create_token_with_refresh_token(self, data, token_valid_for=180,
                                        refresh_token_valid_for=86400):
        """ Create an encrypted JWT with a refresh_token """
        refresh_token = None
        refresh_token = jwt.encode({
            'exp':
                datetime.utcnow() +
                timedelta(seconds=refresh_token_valid_for)},
            self.app_secret).decode("utf-8")
        jwt_token = jwt.encode({
            'data': data,
            'refresh_token': refresh_token,
            'exp': datetime.utcnow() + timedelta(seconds=token_valid_for)},
            self.app_secret)
        return Security.encrypt(jwt_token)

    def verify_refresh_token(self, expired_token) -> bool:
        """  Use request information to validate refresh JWT """
        try:
            decoded_token = jwt.decode(
                Security.decrypt(expired_token),
                self.app_secret,
                options={'verify_exp': False})
            if 'refresh_token' in decoded_token and \
                    decoded_token['refresh_token'] is not None:
                try:
                    jwt.decode(decoded_token['refresh_token'], self.app_secret)
                    self.data = decoded_token
                    return True
                except (Exception, BaseException) as error:
                    self.errors.append(error)
                    return False
        except (Exception, BaseException) as error:
            self.errors.append(error)
            return False
        return False

    def verify_http_auth_refresh_token(self) -> bool:
        """ Use expired token to check refresh token information """
        authorization_token = self.get_http_token()
        if authorization_token is not None:
            if self.verify_refresh_token(authorization_token):
                if self.data is not None:
                    self.data = self.data['data']
                    return True
                return False
            else:
                return False
        return False
