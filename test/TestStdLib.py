'''
@title Test Suite: stdlib Class
@author Carlos Barcelos
@date TODO
'''

import sys  #
sys.path.append("..") # Adds higher directory to python modules path.
import json # Handle JSON files

import unittest # assert(actual, expected)
from src.stdlib import * # Import the stdlib class

# # Test the optionParse function
# class TestOptionParseFunction(unittest.TestCase):
#     def test(self):
#         self.assertEqual(0, 1)
#
# # Test the prettyPrint function
# class TestPrettyPrintFunction(unittest.TestCase):
#     def test(self):
#         self.assertEqual(0, 1)
#
# # Test the itemNameToObject function
# class TestItemNameToObjectFunction(unittest.TestCase):
#     def test(self):
#         self.assertEqual(0, 1)

if __name__ == '__main__':
    unittest.main()
