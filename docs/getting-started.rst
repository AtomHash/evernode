.. _getting-started:

Getting Started
===============

Ready to get started? This page gives a good introduction to EverNode.  It
assumes you already have EverNode installed. If you do not, head over to the
:ref:`installation` section.


Minimal Application
---------------------

The minimal EverNode application looks something like this:

.. code-block:: python

    from evernode.classes import App

    # --- @boot ---
    app_class = App(__name__)  # this is the EverNode app
    app = app_class.app  # this is the Flask app
    # --- @boot ---


    # uWSGI entry point
    if __name__ == '__main__':
        app.run()
