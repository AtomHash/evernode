"""
    User Model
"""
from .base_model import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey


class PasswordResetModel(BaseModel):
    """ Password Reset db Model """

    __tablename__ = 'user_password_resets'
    token = Column(String(1000))
    code = Column(String(70))
    user_id = Column(Integer, ForeignKey('users.id'))

    @classmethod
    def where_token(cls, token):
        """ get by token """
        return cls.query.filter_by(token=token).first()

    @classmethod
    def where_code(cls, code):
        """ get by code """
        return cls.query.filter_by(code=code).first()

    @classmethod
    def where_user_id(cls, user_id):
        """ get by user_id """
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def delete_where_user_id(cls, user_id):
        """ delete by email """
        result = cls.where_user_id(user_id)
        if result is None:
            return None
        result.delete()
        return True
