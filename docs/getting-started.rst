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
    evernode_app = App(__name__)  # this is the EverNode app
    app = evernode_app.app  # this is the Flask app
    # --- @boot ---


    # uWSGI entry point
    if __name__ == '__main__':
        app.run()


Config
------

This section will cover the EverNode config.json file

Overview
```````````

Your EverNode config should look like::

    {
      "NAME": "App Name",
      "DEBUG": true,
      "SERECT": "secret-key-jwt",
      "KEY": "encryption-key",
      "DATETIME": {
        "TIMEZONE": "UTC",
        "DATE_FORMAT": "%Y-%m-%d",
        "TIME_FORMAT": "%H:%M:%S",
        "SEPARATOR": " "
      },
      "DEFAULT_LANGUAGE": "en",
      "HOST": "localhost",
      "SQLALCHEMY_TRACK_MODIFICATIONS": false,
      "SQLALCHEMY_ECHO": true,
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
        "HOST": "smtp.example.com",  # email smtp host
        "PORT": 587,  # port over ssl/tls
        "EMAIL": "noreply@example.com",  # from email
        "NAME": "EverNode",  # from name
        "AUTH": "true",  # login to smtp
        "TRANSPORT": "tls",  # secure layer
        "USERNAME": "noreply@example.com",  # smtp server username
        "PASSWORD": "somePassword" # smtp server password
      },
      "AUTH": {
        "JWT_EXP_SECS": 360,  # JWT validity period
        "FAST_SESSIONS": true,  # don't check session against database
        "MAX_SESSIONS": 1,  # how many active sessions a user can have
        "USERNAME_FIELD": "email",
        "PASSWORD_FIELD": "password",
        "PASSWORD_HASHING": "pbkdf2:sha512"
      },
      "MAX_CONTENT_LENGTH": 2000000,
      "SQLALCHEMY_POOL_SIZE": 100,
      "SQLALCHEMY_POOL_RECYCLE": 280,
      "SQLALCHEMY_BINDS": {
        "DEFAULT": "mysql://db_user:db_password@your-db-ip/db"
      }
    }

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

This section will cover how to setup evernode with uWSGI.

uwsgi.ini
````````````

This will start the uwsgi python process, configure as you want.

Example::

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

Non Hair Losing Settings(this is just an example uwsgi.ini)\:

| :code:`wsgi-file=/srv/app/app.py` set the absolute path to your evernode app.py file.
| :code:`callable=app` app is the variable that Flask is running as in your uwsgi-file.
| :code:`pythonpath=/srv/app/` set this to your root application folder of the evernode_app.
| :code:`pythonpath=/srv/app/` set chdir of uwsgi to root application path


NGINX
-----


NGINX .conf File
```````````````````````````````````````

This section covers a basic nginx conf for evernode. Configure as you want.
| Note - Replace [website-domain] with your domain name.
| Example(/etc/nginx/conf.d/[website-domain].conf)::

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

Generate Self-Signed Certificate
`````````````````````````````````

::

    openssl req -new -sha256 -x509 -newkey rsa:4096 \
    -nodes -keyout [website-domain].key -out [website-domain].crt -days 365

Generate Signing Request Certificate
````````````````````````````````````

::

    openssl req -new -sha256 -newkey rsa:4096 \
    -nodes -keyout [website-domain].key -out [website-domain].csr -days 365
