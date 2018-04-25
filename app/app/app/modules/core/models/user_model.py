"""
    User Model
"""

from evernode.models import BaseUserModel


class UserModel(BaseUserModel):
    """ user db model """

    @classmethod
    def where_id(cls, id):
        """ get enity by id """
        return cls.query.filter_by(id=id).first()

    def __repr__(self):
        """ exclue some attributes on jsonify """
        return super().json()
