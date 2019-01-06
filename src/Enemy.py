'''
@title Text Adventure: Enemy Class
@author Carlos Barcelos
@date 06 January 2019

The enemy class with member veriables and functions.
'''

import src.stdlib as std # Import standard libraries

class Enemy():
    def __init__(self, name, details, resources):
        self.name = name
        enemy = toEnemy(details, resources)
        self.description = enemy['description']
        self.inventory = enemy['inventory']
        self.damage = enemy['damage']
        self.stats = enemy['stats']

    # Overload __str__
    def __str__(self):
        return str(self.name)

    # Convert from an enemy object to a JSON string
    def toJSON(self):
        jData = {}
        jData['name'] = self.name
        jData['description'] = self.description
        jData['inventory'] = []
        for item in self.inventory:
            i = item.dictName
            jData['inventory'].append(i)
        jData['damage'] = self.damage
        jData['stats'] = self.stats
        return jData

# Convert from a JSON string to an enemy object
def toEnemy(details, resources):
    enemy = {}
    enemy['description'] = details['description']
    enemy['inventory'] = []
    for item in details['inventory']:
        i = std.itemNameToObject(item, resources)
        enemy['inventory'].append(i)
    enemy['damage'] = details['damage']
    enemy['stats'] = details['stats']
    return enemy
