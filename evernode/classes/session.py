"""
    Static methods to help handle state-less app sessions
"""
from flask import current_app, g
from ..classes.security import Security
from ..models.session_model import SessionModel


class Session:
    """ Helper class for app state-less sessions """

    @staticmethod
    def create_session_id() -> str:
        """ Create a session token """
        return Security.generate_uuid(2)

    @staticmethod
    def set_current_session(session_id) -> bool:
        """ Add session_id to flask globals for current request """
        try:
            g.session_id = session_id
            return True
        except (Exception, BaseException) as error:
            # catch all on config update
            if current_app.config['DEBUG']:
                print(error)
            return False

    @staticmethod
    def current_session() -> str:
        """ Return session id in app globals, only current request """
        session_id = getattr(g, 'session_id', None)
        if session_id is not None:
            return SessionModel.where_session_id(session_id)
        return None

    @classmethod
    def create_session(cls, session_id, user_id):
        """
        Save a new session to the database
        Using the ['AUTH']['MAX_SESSIONS'] config setting
        a session with be created within the MAX_SESSIONS
        limit. Once this limit is hit, delete the earliest
        session.
        """
        count = SessionModel.count(user_id)
        if count < current_app.config['AUTH']['MAX_SESSIONS']:
            cls.__save_session(session_id, user_id)
            return
        elif count >= current_app.config['AUTH']['MAX_SESSIONS']:
            earliest_session = SessionModel.where_earliest(user_id)
            earliest_session.delete()
            cls.__save_session(session_id, user_id)
            return

    @classmethod
    def __save_session(cls, session_id, user_id):
        session = SessionModel()
        session.user_id = user_id
        session.session_id = session_id
        Session.set_current_session(session_id)
        session.save()
