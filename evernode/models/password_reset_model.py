"""
    User Model
"""
from .base_model import BaseModel
from sqlalchemy import Column, String, Integer


class PasswordResetModel(BaseModel):
    """ Password Reset db Model """

    __tablename__ = 'user_password_resets'
    email = Column(String(255), unique=True)
    code = Column(String(255))
    user_id = Column(Integer)

    @classmethod
    def where_email(cls, email):
        """ get by email """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def delete_where_email(cls, email):
        """ delete by email """
        result = cls.where_email(email)
        if result is None:
            return None
        result.delete()
        return True
