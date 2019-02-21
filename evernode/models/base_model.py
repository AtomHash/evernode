""" sets base db model for applciation """
from flask import current_app
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, text
from .database_model import DatabaseModel
from .json_model import JsonModel


class BaseModel(DatabaseModel, JsonModel):
    """ Adds usefull custom attributes for applciation use """

    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        DateTime,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __init__(self):
        DatabaseModel.__init__(self)

    @classmethod
    def where_id(cls, id):
        """ Get db model by id """
        return cls.query.filter_by(id=id).first()

    def exists(self):
        """ Checks if item already exists in database """
        self_object = self.query.filter_by(id=self.id).first()
        if self_object is None:
            return False
        return True

    def updated(self):
        """ Update updated_at timestamp """
        self.updated_at = datetime.utcnow()
        self.save()

    def delete(self):
        """ Easy delete for db models """
        try:
            if self.exists() is False:
                return None
            self.db.session.delete(self)
            self.db.session.commit()
        except (Exception, BaseException) as error:
            # fail silently
            return None

    def save(self):
        """ Easy save(insert or update) for db models """
        try:
            if self.exists() is False:
                self.db.session.add(self)
            # self.db.session.merge(self)
            self.db.session.commit()
        except (Exception, BaseException) as error:
            if current_app.config['DEBUG']:
                raise error
            return None
