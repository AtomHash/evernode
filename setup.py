import re
from setuptools import setup

with open('evernode/__init__.py', 'r') as init_file:
    version = re.search(r'__version__ = "(.*?)"', init_file.read()).group(1)

f = open("README.md")
try:
    README = f.read()
finally:
    f.close()

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
    long_description=README,
    author='AtomHash',
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
        'flask>=1.1.2',
        'Flask-Cors>=3.0.8',
        'PyMySQL>=0.9.3',
        'Flask-SQLAlchemy>=2.2',
        'ujson>=2.0.3',
        'PyJWT>=1.7.1',
        'cryptography',
        'requests',
        'click',
        'Flask-Migrate',
        'schedule'
    ],
    entry_points={
    'console_scripts': [
        ['evernode=evernode.evernode:main'],
    ]
    },
    classifiers=[])
