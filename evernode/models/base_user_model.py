"""
    User Model
"""

from sqlalchemy import Column, String
from ..classes.security import Security
from ..classes.session import Session
from . import BaseModel, JsonModel


class BaseUserModel(BaseModel, JsonModel):
    """ user db model """

    __abstract__ = True
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    email = Column(String(255), unique=True)
    password = Column(String(255))
    firstname = Column(String(255))
    lastname = Column(String(255))

    @classmethod
    def get_by_username(cls, username):
        """ get db model by username """
        return cls.query.filter_by(email=username).first()

    @classmethod
    def get_by_email(cls, email):
        """ get db model by username """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_id(cls, user_id):
        """ get db user model by id """
        return cls.query.get(user_id)

    def set_password(self, password):
        """ set user password with hash """
        self.password = Security.hash(password)
        self.save()

    @classmethod
    def by_current_session(cls):
        session = Session.current_session()
        if session is None:
            return None
        return cls.get_by_id(session.user_id)

    def __repr__(self, exclude_list=None):
        """ exclue some attributes on jsonify """
        if exclude_list is None:
            exclude_list = ['password', 'updated_at', 'created_at', 'id']
        return super().json(exclude_list)
