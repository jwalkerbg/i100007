# test_core_module_b.py

import unittest
from core import core_module_b

class TestCore_b(unittest.TestCase):
    def test_hello_from_core_module_b(self):
        self.assertEqual(core_module_b.hello_from_core_module_b(),2)

if __name__ == '__main__':
    unittest.main()
