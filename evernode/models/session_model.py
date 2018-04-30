""" db model for sessions """
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from .base_model import BaseModel


class SessionModel(BaseModel):
    """ class to handle db model for session """
    __tablename__ = 'user_sessions'
    session_id = Column(String(255), unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    @classmethod
    def where_session_id(cls, session_id):
        """ Easy way to query by session id """
        try:
            session = cls.query.filter_by(session_id=session_id).one()
            return session
        except (NoResultFound, MultipleResultsFound):
            return None

    @classmethod
    def where_user_id(cls, user_id):
        """ Easy way to query by user id """
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def where_lastest(cls, user_id):
        """ Get lastest session by created_at timestamp """
        return cls.query.filter_by(user_id=user_id)\
            .order_by(cls.created_at.desc()).first()

    @classmethod
    def where_earliest(cls, user_id):
        """ Get earilest session by created_at timestamp """
        return cls.query.filter_by(user_id=user_id)\
            .order_by(cls.created_at.asc()).first()

    @classmethod
    def count(cls, user_id):
        """ Count sessions with user_id """
        return cls.query.with_entities(
            cls.user_id).filter_by(user_id=user_id).count()
