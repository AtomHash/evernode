""" sets base db model for applciation """
from flask import current_app
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from .database_model import DatabaseModel


class BaseModel(DatabaseModel):
    """ adds usefull custom attributes for applciation use """

    __abstract__ = True
    id = Column(Integer, primary_key=True)
    updated_at = Column(DateTime)
    created_at = Column(DateTime)

    def __init__(self):
        DatabaseModel.__init__(self)

    def exists(self):
        """ checks if item already exists in database """
        self_object = self.query.filter_by(id=self.id).first()
        if self_object is None:
            return False
        return True

    def updated(self):
        """ update updated_at timestamp """
        self.updated_at = datetime.utcnow()
        self.save()

    def delete(self):
        """ easy delete for db models """
        try:
            if self.exists() is False:
                return None
            self.db.session.delete(self)
            self.db.session.commit()
        except (Exception, BaseException) as error:
            # fail silently
            return None

    def save(self):
        """ easy save(insert or update) for db models """
        try:
            if self.exists() is False:
                self.db.session.add(self)
            # self.db.session.merge(self)
            self.db.session.commit()
        except (Exception, BaseException) as error:
            if current_app.config['DEBUG']:
                print(error)
            # fail silently
            return None
