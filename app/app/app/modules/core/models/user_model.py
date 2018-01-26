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

    def __repr__(self, exclude_list=None):
        """ exclue some attributes on jsonify """
        exclude_list = [
            'updated_at',
            'created_at',
            'password'] + self.exclude_list
        return super().json(exclude_list)
