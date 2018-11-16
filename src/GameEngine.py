'''
@title Text Adventure: GameEngine Class
@author Carlos Barcelos
@date TODO

The GameEngine class with member veriables and functions.
'''

# A simple way to ask yes or no questions
def questionYesNo(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n)> ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

class GameEngine():
    def __init__(self, map, enemies, player):
        self.map = map
        self.enemies = enemies
        self.player = player
        self.currentRoom = 'Room 1'
        self.isOver = False
        self.verbs = {
        'help' : '[]',
        'look' : 'Examine your surroundings',
        'move' : '[dir] Determine the direction in which to travel',
        'take' : '[item] Take an item found in the world',
        'use' : '[item] Performs an action with a given item',
        'battle' : 'Initiate a battle with an enemy',
        'map' : 'Display the map with a legend',
        'stats' : 'Print the player stats',
        'save' : 'Save your progress and continue',
        'quit' : 'Quit the game'}

    # Promt the user for action
    def prompt(self):
        newInput = input(f'{self.currentRoom} > ')
        self.parse(newInput)

    # Get the action word and additional options
    def parse(self, inStr):
        returnState = False
        returnDict = {'verb': None, 'noun': None}
        words = inStr.split()

        # Reject empty strings
        if inStr:
            # Accept maximum one word after verb
            if len(words) == 1:
                returnDict['verb'] = words[0]
            elif len(words) == 2:
                returnDict['verb'] = words[0]
                returnDict['noun'] = words[1]
            returnState = self.workInputOptions(returnDict['verb'], returnDict['noun'])
        return returnState

    # Work on input and additional options
    def workInputOptions(self, verb, noun):
        if not verb in self.verbs.keys():
            return False

        switcher = {
            'help': lambda: self.help(),
            'look' : lambda: self.look(),
            'move': lambda: self.move(noun),
            'take': lambda: self.take(noun),
            'use': lambda: self.use(noun),
            'battle': lambda: self.battle(noun),
            'map': lambda: self.displayMap(),
            'stats': lambda: self.player.printStats(),
            'save': lambda: self.save(),
            'quit': lambda: self.quit()
        }

        func = switcher.get(verb)
        return func()

    # Move a certain direction from the current room
    def move(self, dir):
        if dir is None:
            print('Move requires a direction input: [north, south, east, west].')
            return False

        try:
            nextRoom = self.map['Map'][self.currentRoom]['Connections'][dir]
            self.currentRoom = self.map['Map'][nextRoom]['Title']
            print(self.map['Map'][self.currentRoom]['Description'])
            return True
        except KeyError:
            print(f"Move '{dir}': Invalid direction.")
            print(f"Possible directions from {self.currentRoom}: {self.map['Map'][self.currentRoom]['Connections']}")
            return False

    # Taken a given item and add it to the player inventory
    def take(self, noun):
        if noun is None:
            print('Take requires a noun as input.')
            return False

        returnState = False
        items = self.map['Map'][self.currentRoom]['Items']

        if noun in items:
            self.map['Map'][self.currentRoom]['Items'].remove(noun)
            self.player.inventory.append(noun)
            print(f'Inventory: {self.player.inventory}')
        else:
            print(f'{noun} is not in {self.currentRoom}')

        return returnState

    # TODO: Use a given item
    def use(self, noun):
        if noun is None:
            print('Must use a specific item.')
            return False

        # Try to use the item from the player inventory
        # Try to use the item from the world
        switcher = {
            'key': False
        }

        action = switcher.get(noun)
        return action

    # Battle an enemy in the room
    # TODO: What if multiple enemies in room
    def battle(self, noun):
        try:
            # Find the enemy in the room
            e = self.enemies[self.currentRoom]
            print(e) # TODO: Pretty print enemy stats

            # TODO: Prompt user for battle wager
            if self.player.battle(e):
                print(f"The battle was won. {e['Name']} was defeated.")
                # TODO: What happens when player wins?
                return True # Player wins battle
            else:
                print(f"The battle was lost. {e['Name']} was victorious.")
                # TODO: What happens when player looses?
                return False # Player looses battle
        except KeyError:
            print(f"There is no enemy '{noun}' in the room")
            return False # The battle was not fought

    # Display the map
    def displayMap(self):
        # TODO: Dispaly map.json as a printable string
        print('MAP')
        return False

    # Look around and get a feel for where you are
    def look(self):
        print(self.map['Map'][self.currentRoom]['Description'])

    # Display help information
    def help(self):
        print(f'===== Action: Usage =====')
        for k, v in self.verbs.items():
            print(f'== {k}: {v}')
        print(f'=====================')

    # Save the player and world status
    def save(self):
        print('Save is not yet implemented.')
        # TODO
        return False

    # Quit the game
    def quit(self):
        if not questionYesNo('Are you sure you want to quit?'):
            return False
        if questionYesNo('Quitting...\nWould you like to save?'):
            self.save()
        self.isOver = True
        return True
