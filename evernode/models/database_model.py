""" generic data model for applciation """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DatabaseModel(db.Model):
    """ abstract class for db models """

    __abstract__ = True
    __bind_key__ = "DEFAULT"
    database = db
