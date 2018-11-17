'''
@title Text Adventure: Player Class
@author Carlos Barcelos
@date TODO

The player class with member veriables and functions.
'''

from random import randint
import colorama # Colored console text
colorama.init(autoreset=True)
# TODO: Consider something like --> print(f'{colorama.Fore.RED}===== ADVENTURE =====')

MAX_EXP = 100

# Set the player stats based on their selected class
def setPlayerStats(pClass):
    # ATK Class
    if pClass == 'Brute':
        stats = {'ATK' : [10, 20], 'INT' : [5, 10], 'DEF' : [0, 5]}
    # INT Class
    elif pClass == 'Scholar':
        stats = {'ATK' : [0, 5], 'INT' : [10, 20], 'DEF' : [5, 10]}
    # DEF Class
    elif pClass == 'Druid':
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

    # Add items to the player inventory
    def gainItems(self, items):
        for i in items:
            print(f'You got: {i}')
            self.inventory.append(i)

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
        eStats = e['Stats'].keys()

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
        selectedStat = ''
        while selectedStat not in eStats:
            selectedStat = input(f'Select stat to use in battle: ')

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
