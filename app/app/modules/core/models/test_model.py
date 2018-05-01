"""
    Test Model
"""

from sqlalchemy import Column, String
from evernode.models import BaseModel


class TestModel(BaseModel):
    """ Test DB model """

    __tablename__ = 'tests'
    name = Column(String(20))
    json_exclude_list = ['id']
