'''
@title Text Adventure: Story Class
@author Carlos Barcelos
@date 23 November 2018

The story class is a generic factory for each of the equipment in the game.
'''

from src.Item import Item # Item super class

class Story(Item):
    def __init__(self, dictName, name, description, text):
        super().__init__(dictName, name, description, "False")
        self.text = text
