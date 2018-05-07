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

    def __init__(self):
        self.app_key = current_app.config['KEY']
        self.app_secret = current_app.config['SERECT']
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

    def create_token(self, data, token_valid_secs=180,
                     refresh_token_valid_days=1) -> str:
        """ Construct a JWT """
        refresh_token = None
        if current_app.config['AUTH']['JWT']['REFRESH_TOKENS_ENABLED']:
            refresh_token = jwt.encode({
                'exp':
                    datetime.utcnow() +
                    timedelta(days=refresh_token_valid_days)},
                self.app_secret).decode("utf-8")
        jwt_token = jwt.encode({
            'data': data,
            'refresh_token': refresh_token,
            'exp': datetime.utcnow() + timedelta(seconds=token_valid_secs)},
            self.app_secret)
        return Security.encrypt(jwt_token)

    def verify_refresh_token(self, expired_token) -> bool:
        """ self.data is populated with old token data if valid """
        try:
            decoded_token = jwt.decode(
                expired_token,
                self.app_secret,
                options={'verify_exp': False})
            if 'refresh_token' in decoded_token and \
                    decoded_token['refresh_token'] is not None:
                try:
                    jwt.decode(decoded_token['refresh_token'], self.app_secret)
                    self.data = decoded_token
                    return True
                except jwt.exceptions.ExpiredSignatureError as e:
                    return False
        except (Exception, BaseException) as e:
            return False
        return False

    def verify_token(self, token) -> bool:
        try:
            self.data = jwt.decode(token, self.app_secret)
            return True
        except (Exception, BaseException) as error:
            return False
        return False

    def verify_http_auth_refresh_token(self) -> bool:
        """ Use expired token to check refresh token information """
        authorization_token = self.get_http_token()
        if authorization_token is not None:
            decrypted_token = Security.decrypt(authorization_token)
            if self.verify_refresh_token(decrypted_token):
                if self.data is not None:
                    self.data = self.data['data']
                    return True
                return False
            else:
                return False
        return False

    def verify_http_auth_token(self) -> bool:
        """ Use request information to validate JWT """
        authorization_token = self.get_http_token()
        if authorization_token is not None:
            decrypted_token = Security.decrypt(authorization_token)
            if self.verify_token(decrypted_token):
                if self.data is not None:
                    self.data = self.data['data']
                    return True
                return False
            else:
                return False
        return False
