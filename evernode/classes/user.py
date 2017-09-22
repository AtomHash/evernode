""" Accomplish common user tasks """

from .auth import Auth
from .jwt import JWT
from .session import Session
from ..models import UserModel
from ..models import SessionModel

class User:
    """ User class """
    auth = Auth
    user_model = None

    def __init__(self, user_model=UserModel):
        self.user_model = user_model
        self.auth = Auth()

    def signin(self) -> dict:
        """
        Easy signin for user objects 
        Using the Auth class that autoloads username and
        password from a post request, validate against a
        user. If successful return {'token': jwtToken, 'user':
        UserModel()} else return None
        """
        username = self.auth.username()
        if username is None:
            return None
        user = self.user_model.get_by_username(username)
        if user is None:
            return None
        user.updated()
        if self.auth.verify(user.password) is True:
            session_id = Session.create_session_id()
            jwt = JWT().create_token(session_id)
            Session.create_session(session_id, user.id)
            return {'token': jwt, 'user': user}
        return None

    def current_user(self):
        """
        ** Get current session and user **
        Uses a session_id to locate user_id
        """
        session = SessionModel.get_by_session_id(Session.current_session())
        if session is None:
            return None
        return self.user_model.get_by_id(session.user_id)