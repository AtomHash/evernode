.. _patterns:

Patterns
==========

This section will cover how to structure your EverNode application.


Folder/File Patterns
---------------------------------------

Covers how you should Structure your EverNode root folder and modules. 


Root Folder Structure
``````````````````````

Your EverNode root should look like this::

    evernode_[app-name]/
        modules/
            ...
        resources/
            lang/
                en/
                    http_messages.lang
            templates/
                emails/
                    ...
                ...
        config.json
        app.py


Module Structure
````````````````````

Your EverNode module should look like this::

    somemodule/
        controllers/
            some_controller.py
            some_ctrl.py  # or ctrl for short
        models/
            some_model.py
            some_mdl.py  # or mdl for short
        resources/
            lang/
                en/
                    language.lang
            templates/
                ...
        __init__.py
        routes.py


Overview Structure
````````````````````````````

Your EverNode app should look like this::

    evernode_[app-name]/
        modules/
            somemodule/
                controllers/
                    some_controller.py
                    some_ctrl.py  # or ctrl for short
                models/
                    some_model.py
                    some_mdl.py  # or mdl for short
                resources/
                    lang/
                        en/
                            language.lang
                    templates/
                        ...
                __init__.py
                routes.py
        resources/
            lang/
                en/
                    http_messages.lang
            templates/
                emails/
                    ...
                ...
        config.json
        app.py