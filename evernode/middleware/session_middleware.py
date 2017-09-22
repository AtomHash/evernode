""" Expending upon JWT and using session tokens in middleware """
from ..classes.middleware import Middleware
from ..classes.json_response import JsonResponse
from ..classes.session import Session
from ..models import SessionModel
from ..classes.jwt import JWT

class SessionMiddleware(Middleware):
    """ Middleware to handle sessions with JWT """

    def condition(self) -> bool:
        """ check JWT, then check session for validity """
        jwt = JWT()
        if jwt.verify_token():
            session = SessionModel.get_by_session_id(jwt.session_id)
            print(jwt.session_id)
            print(str(SessionModel.get_by_session_id(jwt.session_id)))
            print(str(SessionModel))
            if session is None:
                return False
            Session.set_current_session(jwt.session_id)
            return True
        return False

    def create_response(self):
        """ return 401 on invalid tokens """
        self.response = JsonResponse(401).create()