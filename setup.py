from setuptools import setup
setup(
  name = 'evernode',
  packages = ['evernode'],
  version = '0.1',
  description = 'EverNode is built by expanding upon flask by adding great features and easy-to-use modular design.',
  author = 'Dylan Harty',
  author_email = 'me@dylanharty.com',
  url = 'https://github.com/dylanharty/evernode',
  download_url = 'https://github.com/atomhash/evernode/archive/0.1.tar.gz',
  keywords = ['server', 'flask-based', 'restful', 'modular', 'evernode'],
  install_requires=[
    'flask',
    'Flask-Cors==3.0.3',
    'mysqlclient',
    'Flask-SQLAlchemy==2.2',
    'PyJWT',
    'dill',
    'cryptography',
    'requests'
  ],
  classifiers = [],
)