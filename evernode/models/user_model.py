"""
    User Model
"""

from sqlalchemy import Column, String
from ..classes.security import Security
from . import BaseModel, JsonModel

class UserModel(BaseModel, JsonModel):
    """ user db model """

    __tablename__ = 'users'
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

    def __repr__(self, exclude_list=None):
        """ exclue some attributes on jsonify """
        if exclude_list is None:
            exclude_list = ['password', 'updated_at', 'created_at', 'id']
        return super().__repr__(exclude_list)
