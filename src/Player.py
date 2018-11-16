'''
@title Text Adventure: Player Class
@author Carlos Barcelos
@date TODO

The player class with member veriables and functions.
'''
import colorama # Colored console text
colorama.init(autoreset=True)
# TODO: Consider something like --> print(f'{colorama.Fore.RED}===== ADVENTURE =====')

# Set the player stats based on their selected class
def setPlayerStats(pClass):
    # ATK Class
    if pClass == 'ATK Class':
        stats = {'ATK_min': 10, 'DEF_min': 0, 'INT_min': 5,'ATK_max': 20, 'DEF_max': 5, 'INT_max': 10}
    # INT Class
    elif pClass == 'INT Class':
        stats = {'ATK_min': 0, 'DEF_min': 5, 'INT_min': 10,'ATK_max': 5, 'DEF_max': 10, 'INT_max': 20}
    # DEF Class
    elif pClass == 'DEF Class':
        stats = {'ATK_min': 5, 'DEF_min': 10, 'INT_min': 0,'ATK_max': 10, 'DEF_max': 20, 'INT_max': 5}
    return stats

class Player():
    def __init__(self, pName, pClass):
        self.pName = pName
        self.pClass = pClass
        self.inventory = []
        self.level = 0
        self.exp = 0
        self.upgradesAvailable = 0
        self.stats = setPlayerStats(self.pClass)

    # Print the player stats
    def printStats(self):
        print(f'===== {self.pName}: Level {self.level} {self.pClass} =====')
        if self.upgradesAvailable:
            print(f'== EXP ({self.upgradesAvailable}): {self.exp} / 100')
        else:
            print(f'== EXP: {self.exp} / 100')
        print(f'== Inventory: {self.inventory}')
        print(f"== ATK: {self.stats['ATK_min']}..{self.stats['ATK_max']}")
        print(f"== DEF: {self.stats['DEF_min']}..{self.stats['DEF_max']}")
        print(f"== INT: {self.stats['INT_min']}..{self.stats['INT_max']}")
        print(f'=====================')

    # Do battle with some enemy
    def battle(self, e):
        # TODO:
        print('player.battle()')
        return False
