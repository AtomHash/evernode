.. _modules:

Modules
==================

EverNode uses modular design to build out APIs. How you use modules are entirely up to you.
This means that after following the set folder and file names listed below, everything else
is up to you. You can make one giant module for the whole API or many smaller modules ect...

However, our rule of thumb is a module should have one purpose.

**Example:**
So if you have Users for your application, make a :code:`evernode_<app-name>/app/modules/users`
module. This module will handle User logins, signups, password resets, profiles and most things
User Related. 

Creating a Module
-----------------

All modules for EverNode belong in the :code:`evernode_<app-name>/app/modules` folder.

Basic Structure
```````````````

Required folder and file names are as following::

    <module-name>/
        controllers/
            __init__.py
            <ctrl-name>_controller.py
            <ctrl-name>_ctrl.py  # or ctrl for short
        models/
            __init__.py
            <model-name>_model.py
            <model-name>_mdl.py  # or mdl for short
        resources/
            lang/
                en/
                    <file-name>.lang
            templates/
                ...
        __init__.py
        routes.py

Basic Routing
``````````````

There are no standards for routing in EverNode. Just be smart about it. If a module is called :code:`users`,
name the routes users-<route> and the url will be /v1/users/<route>. If you follow this approach create a
'core'/'root' module to have all routes that start at /v1/<route>.

RESTful design, controllers should be used for singular objects(nouns). Each function/route will belong to different
HTTP methods. 

RESTful Example::

    # modules/books/routes.py
    from .controllers import BookController

    routes = [
        {
            'url': '/books/<book_id>',
            'name': 'book-get',
            'methods': ['GET'],
            'function': BookController.get}]
    # -------------------------------------------------------
    # modules/books/models/book_model.py
    from evernode.models import BaseModel

    class BookModel(BaseModel):
    """ Book DB Model """

        __tablename__ = 'books'

    # -------------------------------------------------------
    # modules/books/controllers/book_controller.py
    from flask import current_app # noqa
    from evernode.classes import JsonResponse
    from ..models import BookModel

    class BookController:
        """ RESTful example, BookController """

        @staticmethod
        def get(book_id):
            """ Get a book by id """
            return JsonResponse(200, None, BookModel.where_id(book_id))
