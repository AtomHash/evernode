"""
    Used for password verification
"""
from flask import request, current_app, Flask
from .security import Security


class Auth:
    """ Helper class for creating user based authentication """

    app = Flask
    algo = None
    user_field = ''
    password_field = ''
    __username = None
    __password = None

    def __init__(self):
        self.app = current_app
        self.algo = self.app.config['AUTH']['PASSWORD_HASHING']
        self.user_field = self.app.config['AUTH']['USER_FIELD']
        self.password_field = self.app.config['AUTH']['PASSWORD_FIELD']
        self.collect_fields()

    def collect_fields(self) -> int:
        """ use field values from config.json and collect from request """
        field_count = 0
        request_json = request.get_json()
        if request_json is not None:
            if self.user_field in request_json:
                self.__username = request_json[self.user_field]
                field_count += 1
            if self.password_field in request_json:
                self.__password = request_json[self.password_field]
                field_count += 1
        return field_count

    def username(self) -> str:
        """ return username """
        return self.__username

    def verify(self, hashed_password) -> bool:
        """ check if a hashed password is valid with collected fields """
        if self.collect_fields() == 2:
            return self.verify_password(hashed_password)
        return False

    @staticmethod
    def create_password(clear_text) -> str:
        """ hash clear text """
        return Security.hash(clear_text)

    def verify_password(self, hashed_password) -> bool:
        """ check a password hash """
        return Security.verify_hash(self.__password, hashed_password)
