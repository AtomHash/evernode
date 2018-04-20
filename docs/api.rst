.. _api:

API
===

.. module:: evernode.classes

The technical part of the documentation that covers what certain interfaces do within EverNode.


Classes
---------------------------------------

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
