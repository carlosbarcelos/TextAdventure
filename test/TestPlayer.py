'''
@title Test Suite: Player Class
@author Carlos Barcelos
@date TODO
'''

import sys
sys.path.append("..") # Adds higher directory to python modules path.
import unittest
from src.Player import Player   # Import the Player class

class MyTestCase1(unittest.TestCase):

    # # Only use setUp() and tearDown() if necessary
    # def setUp(self):
    # def tearDown(self):

    def test_feature_one(self):
        self.assertEqual(0, 0)

    def test_feature_two(self):
        self.assertEqual(1, 1)

class MyTestCase2(unittest.TestCase):
    # # Only use setUp() and tearDown() if necessary
    # def setUp(self):
    # def tearDown(self):

    def test_feature_one(self):
        self.assertEqual(0, 1)

    def test_feature_two(self):
        self.assertEqual(1, 0)


if __name__ == '__main__':
    unittest.main()
