from .controllers import CoreController
from evernode.middleware import SessionMiddleware # noqa

routes = [
    {
        'url': '/test',
        'name': 'core-test',
        'methods': ['GET'],
        'function': CoreController.test}]
