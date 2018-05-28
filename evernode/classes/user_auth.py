"""
    Used for password verification
"""
from flask import current_app
from .jwt import JWT
from .form_data import FormData
from .security import Security
from .session import Session


class UserAuth:
    """ Helper class for creating user based authentication """

    algo = None
    user = None
    user_model = None
    username = None
    password = None
    __username_error = None
    __password_error = None
    __username_field = None
    __password_field = None

    def __init__(self, user_model, username_error=None, password_error=None):
        self.__username_field = current_app.config['AUTH']['USERNAME_FIELD']
        self.__password_field = current_app.config['AUTH']['PASSWORD_FIELD']
        self.__username_error = username_error
        self.__password_error = password_error
        self.user_model = user_model
        self.__collect_fields()

    def __collect_fields(self):
        """ Use field values from config.json and collect from request """
        form = FormData()
        form.add_field(self.__username_field, required=True,
                       error=self.__username_error)
        form.add_field(self.__password_field, required=True,
                       error=self.__password_error)
        form.parse()
        self.username = form.values[self.__username_field]
        self.password = form.values[self.__password_field]
        return

    def session(self) -> str:
        """ Generate a session(authorization Bearer) JWT token """
        session_jwt = None
        self.user = self.user_model.where_username(self.username)
        if self.user is None:
            return None
        self.user.updated()  # update timestamp on user access
        if self.verify_password(self.user.password):
            session_id = Session.create_session_id()
            data = {
                'session_id': session_id,
                'user_id': self.user.id,
                'user_email': self.user.email,
            }
            token_valid_for = \
                current_app.config['AUTH']['JWT']['TOKENS']['VALID_FOR'] if \
                'VALID_FOR' in \
                current_app.config['AUTH']['JWT']['TOKENS'] else 180
            if current_app.config['AUTH']['JWT']['REFRESH_TOKENS']['ENABLED']:
                refresh_token_valid_for = \
                    current_app \
                    .config['AUTH']['JWT']['REFRESH_TOKENS']['VALID_FOR'] if \
                    'VALID_FOR' in \
                    current_app.config['AUTH']['JWT']['REFRESH_TOKENS'] else \
                    86400
                session_jwt = JWT().create_token_with_refresh_token(
                    data,
                    token_valid_for,
                    refresh_token_valid_for)
            else:
                session_jwt = JWT().create_token(data, token_valid_for)
            Session.create_session(session_id, self.user.id)
            return session_jwt
        return None

    def verify_password(self, hashed_password) -> bool:
        """ Check a password hash """
        return Security.verify_hash(self.password, hashed_password)
