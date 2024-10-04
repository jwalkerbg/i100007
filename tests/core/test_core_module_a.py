# tests/test_core_module_a.py

import unittest
from core import core_module_a

class TestCore_a(unittest.TestCase):
    def test_hello_from_core_module_a(self):
        self.assertEqual(core_module_a.hello_from_core_module_a(),1)

if __name__ == '__main__':
    unittest.main()
