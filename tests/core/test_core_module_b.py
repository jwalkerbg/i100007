# test_core_module_b.py

import unittest
import core

class TestCore_b(unittest.TestCase):
    def test_hello_from_core_module_b(self):
        self.assertEqual(core.hello_from_core_module_b(),2)
