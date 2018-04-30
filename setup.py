import re
from setuptools import setup

with open('evernode/__init__.py', 'r') as init_file:
    version = re.search(r'__version__ = "(.*?)"', init_file.read()).group(1)

setup(
    name='evernode',
    version=version,
    packages=[
        'evernode',
        'evernode.classes',
        'evernode.decorators',
        'evernode.functions',
        'evernode.middleware',
        'evernode.models',
        'evernode.scripts',
        'evernode.bin',
    ],
    description='EverNode is built by expanding upon flask by adding great features and easy-to-use modular design.', # noqa
    author='AtomHash',
    author_email='me@dylanharty.com',
    url='https://github.com/atomhash/evernode',
    download_url=('https://github.com/atomhash/evernode/'
                  'archive/%s.tar.gz') % (version),
    keywords=[
        'server',
        'flask-based',
        'restful',
        'modular',
        'evernode'
    ],
    install_requires=[
        'flask',
        'Flask-Cors>=3.0.3',
        'mysqlclient',
        'Flask-SQLAlchemy>=2.2',
        'PyJWT',
        'cryptography',
        'requests',
        'click',
        'pyyaml',
        'Flask-Migrate'
    ],
    entry_points={
    'console_scripts': [
        ['evernode=evernode.evernode:main'],
    ]
    },
    classifiers=[])
