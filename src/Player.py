'''
@title Text Adventure: Player Class
@author Carlos Barcelos
@date TODO

The player class with member veriables and functions.
'''

from random import randint # Pseudo-random numbers

MAX_EXP = 100
MIN_STAT_UP = 4
MAX_STAT_UP = 5
MAX_STAT_VAL = 100

# Provide a user propt with a given question and acceptible responses
def optionParse(question, answers):
    while "invalid response":
        prettyAnswers = ' ('
        for i in range(len(answers)):
            prettyAnswers += str(answers[i])
            if not i == len(answers)-1:
                prettyAnswers += '/'

        reply = str(input(question+prettyAnswers+')> '))
        if reply in answers:
            return reply

# Set the player stats based on their selected class
def setPlayerStats(pClass):
    # ATK Class
    if pClass == 'Brute':
        stats = {'ATK' : [10, 20], 'INT' : [5, 10], 'DEF' : [0, 5]}
    # INT Class
    elif pClass == 'Scholar':
        stats = {'ATK' : [0, 5], 'INT' : [10, 20], 'DEF' : [5, 10]}
    # DEF Class
    elif pClass == 'Defender':
        stats = {'ATK' : [5, 10], 'INT' : [0, 5], 'DEF' : [10, 20]}
    return stats

class Player():
    def __init__(self, pName, pClass, inventory=[], level=1, exp=0, upgradesAvailable=0):
        self.pName = pName
        self.pClass = pClass
        self.inventory = inventory
        self.level = level
        self.exp = exp
        self.upgradesAvailable = upgradesAvailable
        self.stats = setPlayerStats(self.pClass)

    # Print the player stats
    def printStats(self):
        print(f'===== {self.pName} =====')
        print(f'== Class: Level {self.level} {self.pClass}')
        if self.upgradesAvailable:
            print(f'== Exp ({self.upgradesAvailable}): {self.exp} / {MAX_EXP}')
        else:
            print(f'== Exp: {self.exp} / {MAX_EXP}')
        print(f"== ATK: {self.stats['ATK'][0]}..{self.stats['ATK'][1]}")
        print(f"== INT: {self.stats['INT'][0]}..{self.stats['INT'][1]}")
        print(f"== DEF: {self.stats['DEF'][0]}..{self.stats['DEF'][1]}")
        print(f'== Inventory: {self.inventory}')
        print(f'=====================')

    # Gain additional Exp
    def gainExp(self, val):
        self.exp = (self.exp + val) % MAX_EXP
        self.level += (self.exp + val) // MAX_EXP
        self.upgradesAvailable += (self.exp + val) // MAX_EXP

    # Trade in one level for for one stat upgrade
    def upgrade(self):
        if self.upgradesAvailable < 1:
            print('You have no upgrades available.')
            return False

        # Prompt which stat to upgrade
        availableStats = []
        for s in ['ATK', 'INT', 'DEF']:
            if self.stats[s][0] != MAX_STAT_VAL and self.stats[s][1] != MAX_STAT_VAL:
                availableStats.append(s)

        if not availableStats:
            print('There are no stats available to upgrade.')
            return False

        selectedStat = optionParse('Select a stat to upgrade:', availableStats)

        # Prompt which attribute to upgrade
        availableAttr = []
        # MIN value cannot be larger than MAX
        if (self.stats[selectedStat][0]+MIN_STAT_UP) < self.stats[selectedStat][1]:
            availableAttr.append('MIN')
        # MAX value cannot be larger than MAX_STAT_VAL
        if (self.stats[selectedStat][1]+MAX_STAT_UP) < MAX_STAT_VAL:
            availableAttr.append('MAX')

        if not availableAttr:
            print(f'There are no attributes available to upgrade for {selectedStat}')
            return False

        selectedAttr = optionParse('Select an attribute to upgrade', availableAttr)

        # Do the upgrade and report to user
        upgradePos = 0 if (selectedAttr=='MIN') else 1
        upgradeVal = MIN_STAT_UP if (selectedAttr=='MIN') else MAX_STAT_UP
        self.stats[selectedStat][upgradePos] += upgradeVal
        self.upgradesAvailable -= 1
        print(f'Successfully upgraded {selectedAttr} attribute of {selectedStat} stat.')
        return True

    # Add items to the player inventory
    def getItems(self, items):
        for i in items:
            print(f'You got: {i}')
            self.inventory.append(i)

    # Check the player inventory for a certain number of an item
    def checkInventory(self, item, quantity):
        # TODO
        return False

    # Do battle with some enemy
    def battle(self, e, statTuple):
        # Enemy battle information
        statType = statTuple[0]
        eStatVal = statTuple[1]

        # Get the players battle value from within the range
        pStatVal = randint(self.stats[statType][0], self.stats[statType][1])

        print(f'=== {statType} Battle ===')
        print(f'= {self.pName}: {pStatVal}')
        print(f'= Enemy: {eStatVal}')
        print(f'==================')

        return pStatVal > eStatVal

    # Start a 'top trumps' battle with an enemy
    def topTrumpBattle(self, e):
        eStats = list(e['Stats'].keys())

        # Report the stats comparison
        # TODO: Make this look nicer
        print('=== Stat Comparison ===')
        print('=      Player | Enemy =')
        for s in eStats:
            pStatMin = self.stats[s][0]
            pStatMax = self.stats[s][1]
            eStat = e['Stats'][s]
            print(f'= {s}: {pStatMin}..{pStatMax} | {eStat}')
        print(f'======================')

        # Ask player which stat to battle
        selectedStat = optionParse('Select stat to use in battle:', eStats)

        # Get the enemy value and return the battle
        statTuple = (selectedStat, e['Stats'][selectedStat])
        return self.battle(e, statTuple)

    # Convert the player data to a JSON data dump
    def toJSON(self):
        jData = {}
        jData['pName'] = self.pName
        jData['pClass'] = self.pClass
        jData['inventory'] = self.inventory
        jData['level'] = self.level
        jData['exp'] = self.exp
        jData['upgradesAvailable'] = self.upgradesAvailable
        jData['stats'] = self.stats
        return jData
