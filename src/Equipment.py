'''
@title Text Adventure: Equipment Class
@author Carlos Barcelos
@date 23 November 2018

The equipment class is a generic factory for each of the equipment in the game.
'''

from src.Item import Item # Item super class

class Equipment(Item):
    def __init__(self, dictName, name, description, position, attribute, value):
        super().__init__(dictName, name, description, "False")
        self.position = position
        self.attribute = attribute
        self.value = value
