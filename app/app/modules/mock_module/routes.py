from .controllers import MockController
from evernode.middleware import SessionMiddleware # noqa

routes = [
    {
        'url': '/hello-world',
        'name': 'hello-world',
        'methods': ['GET'],
        'function': MockController.hello_world}]
