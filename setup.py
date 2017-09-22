from setuptools import setup
setup(
  name = 'evernode',
  version = '0.1.7',
  packages = [
    'evernode',
    'evernode.classes',
    'evernode.decorators',
    'evernode.functions',
    'evernode.helpers',
    'evernode.middleware',
    'evernode.models',
    'evernode.scripts',
  ],
  description = 'EverNode is built by expanding upon flask by adding great features and easy-to-use modular design.',
  author = 'AtomHash',
  author_email = 'me@dylanharty.com',
  url = 'https://github.com/atomhash/evernode',
  download_url = 'https://github.com/atomhash/evernode/archive/0.1.7.tar.gz',
  keywords = ['server', 'flask-based', 'restful', 'modular', 'evernode'],
  install_requires=[
    'flask',
    'Flask-Cors>=3.0.3',
    'mysqlclient',
    'Flask-SQLAlchemy>=2.2',
    'PyJWT',
    'dill',
    'cryptography',
    'requests'
  ],
  classifiers = [],
)