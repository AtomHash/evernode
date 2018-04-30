.. _installation:

Installation
============

EverNode requries a web server and Python3.6. It assumes you already have Python3.6 installed.

Python Version
--------------

We currently only support Python 3.6 and above. Our application replies on certain features only avaible in
python 3.6, such as the secrets module added to core in 3.6.

Python 3.6 & pip
````````````````

**Debian and Ubuntu**

.. code-block:: sh

    wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz && tar xvf Python-3.6.5.tar.xz && cd Python-3.6.5 \
    && ./configure --enable-optimizations --with-ensurepip=install && make -j8 && make altinstall

optional, update default python to python 3.6.

.. code-block:: sh

    update-alternatives --install /usr/bin/python python /usr/local/bin/python3.6 50

Install EverNode
----------------

Within the activated environment, use the following command to install EverNode:

.. code-block:: sh

    pip install evernode

Development Releases
````````````````````

If you want to work with the latest EverNode code before it's released, install or
update the code from the master branch:

.. code-block:: sh

    pip install -U https://github.com/AtomHash/evernode/archive/dev-[version].zip

Install NGINX
----------------

.. code-block:: sh

    sudo apt-get install nginx nginx-extras

Install uWSGI
----------------

.. code-block:: sh

    sudo pip install uwsgi