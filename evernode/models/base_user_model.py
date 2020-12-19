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
    fullname = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(1000))
    json_exclude_list = ['password', 'updated_at', 'created_at', 'id']

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
            'code': Security.random_string(5),  # make unique
            'user_id': user.id},
            token_valid_for=valid_for)
        code = Security.generate_uuid(1) + "-" + Security.random_string(5)
        password_reset_model = PasswordResetModel()
        password_reset_model.token = token
        password_reset_model.code = code
        password_reset_model.user_id = user.id
        password_reset_model.save()
        return code

    @classmethod
    def validate_password_reset(cls, code, new_password):
        """
        Validates an unhashed code against a hashed code.
        Once the code has been validated and confirmed
        new_password will replace the old users password
        """
        password_reset_model = \
            PasswordResetModel.where_code(code)
        if password_reset_model is None:
            return None
        jwt = JWT()
        if jwt.verify_token(password_reset_model.token):
            user = cls.where_id(jwt.data['data']['user_id'])
            if user is not None:
                user.set_password(new_password)
                PasswordResetModel.delete_where_user_id(user.id)
                return user
        password_reset_model.delete()  # delete expired/invalid token
        return None

    @classmethod
    def by_current_session(cls):
        """ Returns current user session """
        session = Session.current_session()
        if session is None:
            return None
        return cls.where_id(session.user_id)
