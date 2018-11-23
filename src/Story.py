'''
@title Text Adventure: Story Class
@author Carlos Barcelos
@date TODO

The story class is a generic factory for each of the equipment in the game.
'''

class Story():
    def __init__(self, name, description, text):
        self.name = name
        self.description = description
        self.text = text

    # Overload __str__
    def __str__(self):
        return str(self.name)
