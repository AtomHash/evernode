# pylint: skip-file
import unittest
import os
from evernode.classes import App


class TestClass(unittest.TestCase):

    app_class = None

    @classmethod
    def setUpClass(cls):
        script_path = os.path.dirname(__file__)
        root_path_file = os.path.join(script_path, 'root_path.txt')
        with open(root_path_file, 'r') as opened_file:
            root_path = opened_file.read().replace('\n', '')
            cls.app_class = App(__name__, root_path=(root_path))

    @classmethod
    def tearDownClass(cls):
        cls.app_class = None
