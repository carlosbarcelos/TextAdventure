'''
@title Text Adventure: Equipment Class
@author Carlos Barcelos
@date TODO

The equipment class is a generic factory for each of the equipment in the game.
'''

class Equipment():
    def __init__(self, name, description, position, attribute, value):
        self.name = name
        self.description = description
        self.position = position
        self.attribute = attribute
        self.value = value

    # Overload __str__
    def __str__(self):
        return str(self.name)
