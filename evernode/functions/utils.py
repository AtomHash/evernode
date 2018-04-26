""" application misc util functions"""
import os


def get_subdirectories(directory):
    """ Get subdirectories without pycache """
    return [name for name in os.listdir(directory)
            if name != '__pycache__'
            if os.path.isdir(os.path.join(directory, name))]


def get_python_path() -> str:
    """ Accurately get python executable """
    python_bin = None
    if os.name == 'nt':
        python_root = os.path.abspath(
            os.path.join(os.__file__, os.pardir, os.pardir))
        python_bin = os.path.join(python_root, 'python.exe')
    else:
        python_root = os.path.abspath(
            os.path.join(os.__file__, os.pardir, os.pardir, os.pardir))
        python = os.__file__.rsplit('/')[-2]
        python_bin = os.path.join(python_root, 'bin', python)
    return python_bin
