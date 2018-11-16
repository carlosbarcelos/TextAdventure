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
        stats = {'ATK_min': 10, 'DEF_min': 0, 'INT_min': 5,'ATK_max': 20, 'DEF_max': 5, 'INT_max': 10}
    # INT Class
    elif pClass == 'Scholar':
        stats = {'ATK_min': 0, 'DEF_min': 5, 'INT_min': 10,'ATK_max': 5, 'DEF_max': 10, 'INT_max': 20}
    # DEF Class
    elif pClass == 'Druid':
        stats = {'ATK_min': 5, 'DEF_min': 10, 'INT_min': 0,'ATK_max': 10, 'DEF_max': 20, 'INT_max': 5}
    return stats

class Player():
    def __init__(self, pName, pClass):
        self.pName = pName
        self.pClass = pClass
        self.inventory = []
        self.level = 1
        self.exp = 0
        self.upgradesAvailable = 0
        self.stats = setPlayerStats(self.pClass)

    # Print the player stats
    def printStats(self):
        print(f'===== {self.pName} =====')
        print(f'== Class: Level {self.level} {self.pClass}')
        if self.upgradesAvailable:
            print(f'== Exp ({self.upgradesAvailable}): {self.exp} / {MAX_EXP}')
        else:
            print(f'== Exp: {self.exp} / {MAX_EXP}')
        print(f"== ATK: {self.stats['ATK_min']}..{self.stats['ATK_max']}")
        print(f"== DEF: {self.stats['DEF_min']}..{self.stats['DEF_max']}")
        print(f"== INT: {self.stats['INT_min']}..{self.stats['INT_max']}")
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
        pStatVal = randint(self.stats[f'{statType}_min'], self.stats[f'{statType}_max'])

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
            pStatMin = self.stats[f'{s}_min']
            pStatMax = self.stats[f'{s}_min']
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
