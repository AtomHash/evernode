""" Expending upon JWT and using session tokens in middleware """
from flask import current_app
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
        if jwt.verify_http_auth_token():
            if not current_app.config['AUTH']['FAST_SESSIONS']:
                session = SessionModel.where_session_id(
                    jwt.data['session_id'])
                if session is None:
                    return False
            Session.set_current_session(jwt.data['session_id'])
            return True
        return False

    def create_response(self):
        """ return 401 on invalid tokens """
        self.response = JsonResponse(401)
