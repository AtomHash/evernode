""" decorator for loading custom middleware """
import copy
from functools import wraps
from flask import request
from ..classes import JsonResponse


def middleware(func):
    """ Executes routes.py route middleware """
    @wraps(func)
    def parse(*args, **kwargs):
        """ get middleware from route, execute middleware in order """
        middleware = copy.deepcopy(kwargs['middleware'])
        kwargs.pop('middleware')
        if request.method == "OPTIONS":
            # return 200 json response for CORS
            return JsonResponse(200)
        if middleware is None:
            return func(*args, **kwargs)
        for mware in middleware:
            ware = mware()
            if ware.status is False:
                return ware.response
            return func(*args, **kwargs)
    return parse
