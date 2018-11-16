'''
@title Text Adventure: Item Class
@author Carlos Barcelos
@date TODO

The item class is a generic factory for each of the items in the game.
'''

class Item():
    def __init__(self, name, description, isUsable, uses):
        self.name = name
        self.description = description
        self.isUsable = isUsable
        self.uses = uses

    # Overload __str__
    def __str__(self):
        return f'{self.name}: {self.description}'
