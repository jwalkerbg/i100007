# test_utilities.py

import unittest

from pymodule import utils

class TestUtils(unittest.TestCase):
    def test_hello_from_utils(self):
        self.assertEqual(utils.hello_from_utils(),None)
