.. _folders:

Folder Structure
================

This section will cover how to structure your EverNode application.


Overview Structure
````````````````````````````

Your EverNode app should look like this::

    evernode_<app-name>/
        app/
            modules/
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
        docker/
        logs/
        public/
            static/
        uploads/
        uwsgi.ini

Root Structure
``````````````````````

Your EverNode root should look like this::

    evernode_<app-name>/
        app/
        docker/
        logs/
        public/
            static/
        uploads/
        uwsgi.ini

Module Structure
````````````````````

Your EverNode module should look like this::

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