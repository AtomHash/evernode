""" static methods to help handle state-less app sessions """
import secrets
from flask import current_app
from ..models.session_model import SessionModel


class Session:
    """ helper class for app state-less sessions """

    @staticmethod
    def create_session_id() -> str:
        """ Create a session token """
        return secrets.token_hex() + secrets.token_hex()

    @staticmethod
    def set_current_session(session_id) -> bool:
        """ Add SESSION_ID to current_app config with session_id """
        try:
            current_app.config.update(SESSION_ID=session_id)
            return True
        except (Exception, BaseException) as error:
            """ catch all on config update """
            if current_app.config['DEBUG']:
                print(error)
            return False

    @staticmethod
    def current_session() -> str:
        """ return session id in app config, only current user """
        if 'SESSION_ID' in current_app.config:
            return SessionModel.get_by_session_id(
                current_app.config['SESSION_ID'])
        return None

    @classmethod
    def create_session(cls, session_id, user_id):
        """
        save a new session to the database
        Using the ['AUTH']['MAX_SESSIONS'] config setting
        a session with be created within the MAX_SESSIONS
        limit. Once this limit is hit, delete the earliest
        session.
        """
        count = SessionModel.count(user_id)
        if count < current_app.config['AUTH']['MAX_SESSIONS']:
            cls.__save_session__(session_id, user_id)
            return
        elif count >= current_app.config['AUTH']['MAX_SESSIONS']:
            earliest_session = SessionModel.get_earliest()
            earliest_session.delete()
            cls.__save_session__(session_id, user_id)
            return

    @classmethod
    def __save_session__(cls, session_id, user_id):
        session = SessionModel()
        session.user_id = user_id
        session.session_id = session_id
        Session.set_current_session(session_id)
        session.save()
