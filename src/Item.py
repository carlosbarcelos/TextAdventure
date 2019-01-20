'''
@title Text Adventure: Item Class
@author Carlos Barcelos
@date 25 November 2018

The item class is a generic factory for each of the items in the game.
'''

# Convert string-boolean value to a boolean-boolean value
def stringToBool(strBool):
    return strBool == 'True'

class Item():
    def __init__(self, dictName, name, description, usable):
        self.dictName = dictName
        self.name = name
        self.description = description
        self.usable = stringToBool(usable)

    # Overload __str__
    def __str__(self):
        return str(self.name)
