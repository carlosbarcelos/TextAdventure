'''
@title Test Suite: GameEngine Class
@author Carlos Barcelos
@date TODO
'''

import sys  #
sys.path.append("..") # Adds higher directory to python modules path.
import json # Handle JSON files

import unittest # assert(actual, expected)
from src.Achievements import Achievements # Import the Achievements class
from src.GameEngine import GameEngine # Import the GameEngine class
from src.Player import Player         # Import the Player class

'''
class MyTestCase1(unittest.TestCase):

    # # Only use setUp() and tearDown() if necessary
    # def setUp(self):
    # def tearDown(self):

    def test_feature_one(self):
        self.assertEqual(0, 0)

    def test_feature_two(self):
        self.assertEqual(1, 1)
'''

def getGameEngine():
        # Get the map
        with open('test/testMap.json') as f:
            m = json.load(f)
        # Get the player
        with open('test/testPlayer.json') as f:
            pJSON = json.load(f)
        p = Player(pJSON['pName'], pJSON['pClass'], pJSON['inventory'], pJSON['equipment'], \
            pJSON['level'], pJSON['hp'], pJSON['exp'], pJSON['expRate'], pJSON['gold'], pJSON['goldRate'], \
            pJSON['upgradesAvailable'], pJSON['stats'])
        # Get the achievements
        with open('test/testAchievement.json') as f:
            aJSON = json.load(f)
        a = Achievements(aJSON)

        # Build the resources/lookup tables that the game needs
        r = {}
        with open('resources/items.json') as f:
            r['items'] = json.load(f)
        with open('resources/equipment.json') as f:
            r['equipment'] = json.load(f)
        with open('resources/story.json') as f:
            r['story'] = json.load(f)

        return GameEngine(m, p, a, r)

# Test the print function
class TestHelpFunction(unittest.TestCase):
    def setUp(self):
        self.ge = getGameEngine()

    # GameEngine: help function
    def testHelp(self):
        self.assertEqual(self.ge.help(), True)

    # GameEngine: look function
    def testLook(self):
        self.assertEqual(self.ge.look(), True)

    # GameEngine: map function
    def testMap(self):
        self.assertEqual(self.ge.displayMap(), True)

# Test the examine function
class TestExamineFunction(unittest.TestCase):
    def setUp(self):
        self.ge = getGameEngine()

    def testExamineSuccess(self):
        res = self.ge.examine('object', '1')
        self.assertEqual(res, True)

    def testExamineNoInput(self):
        res = self.ge.examine('', '')
        self.assertEqual(res, False)

    def testExamineInvalidItem(self):
        res = self.ge.examine('invalid', '')
        self.assertEqual(res, False)

    def testExamineNoItems(self):
        self.ge.move('north')
        res = self.ge.examine('object', '1')
        self.assertEqual(res, False)

    def testExamineWeirdInputs(self):
        res = self.ge.examine(' object ', ' 1 ')
        self.assertEqual(res, True)

# Test the move function
class TestMoveFunction(unittest.TestCase):
    def setUp(self):
        self.ge = getGameEngine()

    def testMoveSuccess(self):
        res = self.ge.move('north')
        self.assertEqual(res, True)

    def testMoveNoInput(self):
        res = self.ge.move('')
        self.assertEqual(res, False)

    def testMoveInvalidInput(self):
        res = self.ge.move('InVaLiD')
        self.assertEqual(res, False)

    def testMoveNoConnection(self):
        res = self.ge.move('south')
        self.assertEqual(res, False)

    def testMoveRecentlyOpenedRoom(self):
        res = self.ge.move('') # TODO
        self.assertEqual(res, True)

# Test the take function
class TestTakeFunction(unittest.TestCase):
    def setUp(self):
        self.ge = getGameEngine()

    def testTakeSuccess(self):
        res = self.ge.take('health', ['potion'])
        self.assertEqual(res, True)

    def testTakeSingleWord(self):
        res = self.ge.take('key', '')
        self.assertEqual(res, True)

    def testTakeNoInput(self):
        res = self.ge.take('', '')
        self.assertEqual(res, False)

    def testTakeInvalidInput(self):
        res = self.ge.take('InVaLiD', 'InPuT')
        self.assertEqual(res, False)

    def testTakeItemNotInRoom(self):
        res = self.ge.take('experience', 'gem')
        self.assertEqual(res, False)

# TODO Test the use function
class TestUseFunction(unittest.TestCase):
    def testUseSuccess(self):
        self.assertEqual(0, 1)

# Test the battle function
class TestBattleFunction(unittest.TestCase):
    def setUp(self):
        self.ge = getGameEngine()

    def testBattleSuccess(self):
        res = self.ge.battle('e3')
        self.assertEqual(res, True)

    # def testBattleTopTrumpsSuccess(self):
    #     res = self.ge.battle('e1')
    #     self.assertEqual(res, True) # TODO

    def testBattleFailure(self):
        initialHealth = self.ge.player.hp
        res = self.ge.battle('e2')
        self.assertEqual(res, False)
        self.assertEqual(initialHealth-5, self.ge.player.hp)

    def testBattleNoInput(self):
        res = self.ge.battle('')
        self.assertEqual(res, False)

    def testBattleInvalidInput(self):
        res = self.ge.battle('InVaLiD')
        self.assertEqual(res, False)

    def testBattleInvalidEnemy(self):
        res = self.ge.battle('e10')
        self.assertEqual(res, False)

# Test the read function
class TestReadFunction(unittest.TestCase):
    def setUp(self):
        self.ge = getGameEngine()

    def testReadSuccess(self):
        self.ge.take('log', ['1'])
        res = self.ge.readStory('log', ['1'])
        self.assertEqual(res, True)

    def testReadNoInput(self):
        res = self.ge.readStory('', '')
        self.assertEqual(res, False)

    def testReadNotInInventory(self):
        res = self.ge.readStory('log', ['2'])
        self.assertEqual(res, False)

# Test the save function
class TestSaveFunction(unittest.TestCase):
    def testSaveSuccess(self):
        self.assertEqual(0, 1)

# Test the quit function
class TestQuitFunction(unittest.TestCase):
    def testQuitSuccess(self):
        self.assertEqual(0, 1)

# Test that functions get handed off to the player class
# Player functions: battle
# Player functions: take
# Player functions: equip
# Player functions: unequip
# Player functions: stats
# Player functions: inventory
# Player functions: equipment
# Player functions: upgrade
# Player functions: achievements

if __name__ == '__main__':
    unittest.main()
