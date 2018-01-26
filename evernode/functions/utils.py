""" application misc util functions"""
import os


def get_subdirectories(directory):
    """ get subdirectories without pycache """
    return [name for name in os.listdir(directory)
            if name != '__pycache__'
            if os.path.isdir(os.path.join(directory, name))]
