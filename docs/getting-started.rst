.. _getting-started:

Getting Started
===============

Ready to get started? This page gives a good introduction to EverNode.  It
assumes you already have EverNode, Python3.6, uWSGI and NGINX installed. If you do not, head over to the
:ref:`installation` section.


Minimal Application
-------------------

The minimal EverNode application looks something like this:

.. code-block:: python

    from evernode.classes import App

    # --- @boot ---
    evernode_app = App(__name__)  # this is the EverNode app
    app = evernode_app.app  # this is the Flask app
    # --- @boot ---


    # uWSGI entry point
    if __name__ == '__main__':
        app.run()


EverNode Console
-------------------

New App
```````

You can easily create a new EverNode application by using the :code:`evernode init` command via command line.

.. code-block:: sh

    $ evernode init <app-name>

Once the files have been downloaded they will be in a evernode\_<app-name> folder, relative to where the command was run.
It's optional to download the docker files and the mock module.

    1. Update the database connection string in the config file. :code:`evernode_<app-name>/app/config.json`
  
        .. code-block:: text

            "SQLALCHEMY_BINDS": {
                "DEFAULT": "mysql://<db_user>:<password>@<host>/<db_name>"
            }

        Note:
            * EverNode can run without a database, but cannot use JWT sessions / DB Models.
            * You can change :code:`mysql` to your odbc database connector.

    2. Process models and Migrate the database. Navigate to :code:`evernode_<app-name>/app`. Run the following commands in the terminal:
  
        .. code-block:: sh

            $ flask db init
            $ flask db migrate
            $ flask db upgrade

    3. If you downloaded the Docker files, you can run :code:`docker-compose up --build` in the :code:`evernode_<app-name>/docker` directory.

        * Please add the host below to your HOSTS file::

            127.0.0.1           api.localhost

    4. If you downloaded the Mock Module, once the docker image has started you can navigate to :code:`https://api.localhost/v1/hello-world`.

New Module
``````````

You can easily create new EverNode modules by using the :code:`evernode module init` command via command line. 

**WARNING:** Make sure to navigate to the :code:`app/modules` folder. This command will make a folder relative to your command line :code:`cd` location.

.. code-block:: sh

    $ evernode module init <module-name>

Config
------

This section covers the configuration of EverNode. Applications need some kind of configuration.
There are different settings you might want to change depending on the application environment like toggling the debug mode,
setting the secret key, and other such environment-specific things.

Overview
`````````

Example \| *config.json*

::

    {
      "NAME": "<app-name>",
      "DEBUG": true,
      "SERECT": "<generate-fernet-key>",
      "KEY": "<generate-fernet-key>",
      "DEFAULT_LANGUAGE": "en",
      "DATETIME": {
        "TIMEZONE": "UTC",
        "DATE_FORMAT": "%Y-%m-%d",
        "TIME_FORMAT": "%H:%M:%S",
        "SEPARATOR": " "
      },
      "API": {
        "VERSION": "1",
        "PREFIX": "v{v}"
      },
      "UPLOADS": {
        "FOLDER": "/srv/uploads",
        "EXTENSIONS": [
          "png",
          "jpg"
        ]
      },
      "CORS": {
        "ALLOW_HEADERS": [
          "Origin",
          "Content-Type",
          "Accept",
          "Authorization",
          "X-Request-With",
          "Content-Language"
        ]
      },
      "EMAIL": {
        "HOST": "<stmp.example.com>",
        "PORT": 587,
        "EMAIL": "<example@atomhash.org>",
        "NAME": "<email-sending-name>",
        "AUTH": "true",
        "TRANSPORT": "tls",
        "USERNAME": "<example@atomhash.org>",
        "PASSWORD": "<password>"
      },
      "AUTH": {
        "JWT": {
          "TOKENS": {
            "VALID_FOR": 7200
          },
          "REFRESH_TOKENS": {
            "ENABLED": false,
            "VALID_FOR": 86400
          }
        },
        "FAST_SESSIONS": false,
        "MAX_SESSIONS": 3,
        "USERNAME_FIELD": "<http-body-form-username-field-name>",
        "PASSWORD_FIELD": "<http-body-form-password-field-name>",
        "PASSWORD_HASHING": "pbkdf2:sha512"
      },
      "MAX_CONTENT_LENGTH": 2000000,
      "SQLALCHEMY_TRACK_MODIFICATIONS": false,
      "SQLALCHEMY_ECHO": true,
      "SQLALCHEMY_POOL_SIZE": 100,
      "SQLALCHEMY_POOL_RECYCLE": 280,
      "SQLALCHEMY_BINDS": {
        "DEFAULT": "mysql://api_user:password@ip/api"
      }
    }
    
**Ambiguous Types**

| DATE_FORMAT is strftime python format
| TIME_FORMAT is strftime python format
| MAX_CONTENT_LENGTH(FLASK) is in bytes
| JWT TOKENS -> VALID_FOR is in seconds
| JWT REFRESH_TOKENS -> VALID_FOR is in seconds

Debug Values
````````````

The following settings should be used in a development enviroment::

    {
      "DEBUG": true,
      "SQLALCHEMY_TRACK_MODIFICATIONS": false,
      "SQLALCHEMY_ECHO": true,
    }

Production Values
`````````````````

The following settings are values best suited for a production enviroment::

    {
      "DEBUG": false,
      "SQLALCHEMY_TRACK_MODIFICATIONS": false,
      "SQLALCHEMY_ECHO": false,
    }


uWSGI
------

This section will cover how to setup EverNode with uWSGI.

uwsgi.ini
````````````

Example \| *uwsgi.ini*

::

    [uwsgi]
    uid=www-data
    gid=www-data
    chdir=/srv/app
    pythonpath=/srv/app/
    wsgi-file=/srv/app/app.py
    callable=app
    master=true
    processes=4
    threads=2
    socket=/run/uwsgi/uwsgi.sock
    chmod-socket=664
    max-requests=5000
    py-autoreload=1
    logto = /srv/logs/%n.log
    ignore-sigpipe=true
    ignore-write-errors=true
    disable-write-exception=true

* :code:`wsgi-file=/srv/app/app.py` set the absolute path to your evernode app.py file.
* :code:`callable=app` app is the variable that Flask is running as in your uwsgi-file.
* :code:`pythonpath=/srv/app/` set this to your root application folder of the evernode_app.
* :code:`pythonpath=/srv/app/` set chdir of uwsgi to root application path

Learn more about uWSGI configuration: `<http://uwsgi-docs.readthedocs.io/en/latest/Configuration.html>`_.

NGINX
-----

This section covers a basic nginx conf to start hosting your API.

Virtual Host File
```````````````````````````````````````

Example \| /etc/nginx/conf.d/*[website-domain].conf*
::

    server {
        listen 80;
        listen 443 ssl;
        server_name [website-domain];
        ssl_certificate     ssls/[website-domain].crt;
        ssl_certificate_key ssls/[website-domain].key;
        root /srv/public;

        location / {
            include uwsgi_params;
            uwsgi_pass unix:///run/uwsgi/uwsgi.sock;
            uwsgi_read_timeout 1800;
            uwsgi_send_timeout 1800;
        }

        location ~ /\.ht {
            deny all;
        }
    }

Replace :code:`[website-domain]` with your domain name.

Learn more about NGINX configuration: `<http://nginx.org/en/docs/beginners_guide.html>`_.

Generate Self-Signed Certificate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    openssl req -new -sha256 -x509 -newkey rsa:4096 \
    -nodes -keyout [website-domain].key -out [website-domain].crt -days 365

Replace :code:`[website-domain]` with your domain name.

Generate Signing Request Certificate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    openssl req -new -sha256 -newkey rsa:4096 \
    -nodes -keyout [website-domain].key -out [website-domain].csr -days 365

Replace :code:`[website-domain]` with your domain name.
