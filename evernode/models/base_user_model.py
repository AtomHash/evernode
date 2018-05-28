"""
    User Model
"""

from sqlalchemy import Column, String
from ..classes.security import Security
from ..classes.session import Session
from ..classes.jwt import JWT
from .base_model import BaseModel
from .password_reset_model import PasswordResetModel


class BaseUserModel(BaseModel):
    """ User db model """

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    email = Column(String(255), unique=True)
    password = Column(String(255))
    firstname = Column(String(255))
    lastname = Column(String(255))
    json_exclude_list = ['password', 'updated_at', 'created_at', 'id']

    @classmethod
    def where_username(cls, username):
        """ Get db model by username """
        return cls.query.filter_by(email=username).first()

    @classmethod
    def where_email(cls, email):
        """ Get db model by email """
        return cls.query.filter_by(email=email).first()

    def set_password(self, password):
        """ Set user password with hash """
        self.password = Security.hash(password)
        self.save()

    @classmethod
    def create_password_reset(cls, email, valid_for=3600) -> str:
        """
        Create a password reset request in the user_password_resets
        database table. Hashed code gets stored in the database.
        Returns unhashed reset code
        """
        user = cls.where_email(email)
        if user is None:
            return None
        PasswordResetModel.delete_where_user_id(user.id)
        token = JWT().create_token({
            'code': Security.random_string(5),
            'user_id': user.id},
            token_valid_for=valid_for)
        password_reset_model = PasswordResetModel()
        password_reset_model.token = token
        password_reset_model.user_id = user.id
        password_reset_model.save()
        return token

    @classmethod
    def validate_password_reset(cls, token, new_password):
        """
        Validates an unhashed code against a hashed code.
        Once the code has been validated and confirmed
        new_password will replace the old users password
        """
        jwt = JWT()
        if jwt.verify_token(token):
            print(jwt.data)
            user = cls.where_id(jwt.data['data']['user_id'])
            if user is not None:
                password_reset_model = \
                    PasswordResetModel.where_user_id(user.id)
                if password_reset_model is None:
                    return False
                user.set_password(new_password)
                PasswordResetModel.delete_where_user_id(user.id)
                return True
        return False

    @classmethod
    def by_current_session(cls):
        """ Returns current user session """
        session = Session.current_session()
        if session is None:
            return None
        return cls.where_id(session.user_id)
