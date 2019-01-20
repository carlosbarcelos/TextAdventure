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

# TODO
# # Test the itemNameToObject function
# class TestItemNameToObjectFunction(unittest.TestCase):
#     def test(self):
#         self.assertEqual(0, 1)

# Test the itemNameToObject function
class TestGetOppDirFunction(unittest.TestCase):
    def testNorth(self):
        dir = 'north'
        oppDir = getOppDir(dir)
        self.assertEqual(oppDir, 'south')

    def testSouth(self):
        dir = 'south'
        oppDir = getOppDir(dir)
        self.assertEqual(oppDir, 'north')

    def testWest(self):
        dir = 'west'
        oppDir = getOppDir(dir)
        self.assertEqual(oppDir, 'east')

    def testEast(self):
        dir = 'east'
        oppDir = getOppDir(dir)
        self.assertEqual(oppDir, 'west')

    def testNone(self):
        dir = 'not a dir'
        oppDir = getOppDir(dir)
        self.assertEqual(oppDir, None)

if __name__ == '__main__':
    unittest.main()
