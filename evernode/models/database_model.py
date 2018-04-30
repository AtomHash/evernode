""" generic data model for applciation """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DatabaseModel(db.Model):
    """ Abstract class for db models """

    __abstract__ = True
    __bind_key__ = "DEFAULT"
    db = db
