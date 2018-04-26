.. _api:

API
===

The technical part of the documentation that covers what certain interfaces do within EverNode.


Classes
---------------------------------------
.. module:: evernode.classes

This part of the documentation covers all the classes of EverNode.

App
````````````````````

.. autoclass:: App
   :members:
   :inherited-members:

   .. attribute:: prefix

      Makes every URL require ending prefix. eg. prefix="v1", https://example.com/v1/

   .. attribute:: middleware

      Set before middleware for all routes(environ, wsgi app)

   .. attribute:: root_path

      Set a root path with an absolute system folder path

   .. attribute:: config_path

      Set a config path(config.json) with an absolute system folder path


BaseResponse
````````````````````

.. autoclass:: BaseResponse
   :members:
   :inherited-members:

Email
````````````````````

.. autoclass:: Email
   :members:
   :inherited-members:

FormData
````````````````````

.. autoclass:: FormData
   :members:
   :inherited-members:

Json
````````````````````

.. autoclass:: Json
   :members:
   :inherited-members:

JsonResponse
````````````````````

.. autoclass:: JsonResponse
   :members:
   :inherited-members:

JWT
````````````````````

.. autoclass:: JWT
   :members:
   :inherited-members:

Middleware
````````````````````

.. autoclass:: Middleware
   :members:
   :inherited-members:

Render
````````````````````

.. autoclass:: Render
   :members:
   :inherited-members:

Security
````````````````````

.. autoclass:: Security
   :members:
   :inherited-members:

Session
````````````````````

.. autoclass:: Session
   :members:
   :inherited-members:

Translator
````````````````````

.. autoclass:: Translator
   :members:
   :inherited-members:

UserAuth
````````````````````

.. autoclass:: UserAuth
   :members:
   :inherited-members:


Models
---------------------------------------
.. module:: evernode.models

This part of the documentation covers all the models of EverNode.

BaseModel
````````````````````

.. autoclass:: BaseModel
   :members:
   :inherited-members:

BaseUserModel
````````````````````

.. autoclass:: BaseUserModel
   :members:
   :inherited-members:

DatabaseModel
````````````````````

.. autoclass:: DatabaseModel
   :members:
   :inherited-members:

JsonModel
````````````````````

.. autoclass:: JsonModel
   :members:
   :inherited-members:

PasswordResetModel
````````````````````

.. autoclass:: PasswordResetModel
   :members:
   :inherited-members:

ResponseModel
````````````````````

.. autoclass:: ResponseModel
   :members:
   :inherited-members:

SessionModel
````````````````````

.. autoclass:: SessionModel
   :members:
   :inherited-members:


Decorators
---------------------------------------
.. module:: evernode.decorators

This part of the documentation covers all the decorators of EverNode.

@middleware
````````````````````

.. autofunction:: middleware

Functions
---------------------------------------
.. module:: evernode.functions

This part of the documentation covers all the functions of EverNode.

get_subdirectories()
````````````````````

.. autofunction:: get_subdirectories

get_python_path()
````````````````````

.. autofunction:: get_python_path

Scripts
---------------------------------------
.. module:: evernode.scripts

This part of the documentation covers all the scripts of EverNode.

SendEmail
````````````````````

.. autoclass:: SendEmail
   :members:
   :inherited-members:


