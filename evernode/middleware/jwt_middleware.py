"""
    Middleware for JWT
"""
from ..classes.middleware import Middleware
from ..classes.json_response import JsonResponse
from ..classes.jwt import JWT


class JWTMiddleware(Middleware):
    """ Middleware to conditionally accept a JWT request """

    def condition(self) -> bool:
        """ Check a JWT token """
        return JWT().verify_http_authorization_token()

    def create_response(self):
        """ is condition false, return 401"""
        self.response = JsonResponse(401)
