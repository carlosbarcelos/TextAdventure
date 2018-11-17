'''
@title Text Adventure: GameEngine Class
@author Carlos Barcelos
@date TODO

The GameEngine class with member veriables and functions.
'''

import glob                   # Search files/directories
import json                   # Handle JSON files
import networkx as nx         # Directed graph
from datetime import datetime # Current datetime

BATTLE_EXP = 5
EXPLORE_EXP = 5
TBD_DEF_EXP = 5

# A simple way to ask yes or no questions
def questionYesNo(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n)> ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

class GameEngine():
    def __init__(self, map, player):
        self.map = map
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
            nextRoom = self.map[self.currentRoom]['Connections'][dir]
            self.currentRoom = self.map[nextRoom]['Title']
            self.look()
            return True
        except KeyError:
            print(f"Move '{dir}': Invalid direction.")
            print(f"Possible directions from {self.currentRoom}: {self.map[self.currentRoom]['Connections']}")
            return False

    # Taken a given item and add it to the player inventory
    def take(self, noun):
        if noun is None:
            print('Take requires a noun as input.')
            return False

        returnState = False
        items = self.map[self.currentRoom]['Items']

        if noun in items:
            self.map[self.currentRoom]['Items'].remove(noun)
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
    # TODO: Return the victor of the battle or None if no battle took place
    def battle(self, noun):
        # A battle cannot take place without an enemy
        if not self.map[self.currentRoom]['Enemies']:
            print('There are no enemies in this room to battle')
            return False

        # An enemy must be selected to start a battle
        if noun is None:
            print('Select an enemy to battle.')
            return None

        # Find the enemy in the room
        for e in self.map[self.currentRoom]['Enemies']:
            if e['Name'] == noun:
                # If the enemy has move than one stat, start topTrumpBattle()
                if len(e['Stats']) > 1:
                    isVictorious = self.player.topTrumpBattle(e)

                # Else, start a normal battle
                else:
                    isVictorious = self.player.battle(e, e['Stats'].popitem())

                # Perform after action report
                if isVictorious:
                    print('You won that battle.')
                    # Reward the player for victory
                    self.player.gainExp(BATTLE_EXP)
                    if e['Inventory']:
                        self.player.getItems(e['Inventory'])
                    self.map[self.currentRoom]['Enemies'].remove(e)
                    return True

                else:
                    print('You lost that battle.')
                    # Add the enemy back to the
                    return False

        print(f"The enemy '{noun}' is not in this room")
        return None

    # Display the map
    # TODO: Dispaly map.json as a printable string
    def displayMap(self):
        print('Display map not yet implemented')
        '''
        mapGraph = nx.DiGraph()

        # Make a directed graph structure from the map JSON
        mapGraph.add_nodes_from(map['Map'].keys())
        for room in mapGraph.nodes():
            for dest in map['Map'][room]['Connections'].values():
                mapGraph.add_edge(room, dest)
        '''
        return False

    # Look around and get a feel for where you are
    def look(self):
        print(self.map[self.currentRoom]['Description'])
        enemyList = self.map[self.currentRoom]['Enemies']
        if enemyList:
            enemyNames = [e['Name'] for e in enemyList]
            print(f'There are a few enemies here: {enemyNames}')
        else:
            print('There are no enemies in this room.')

    # Display help information
    def help(self):
        print(f'===== Action: Usage =====')
        for k, v in self.verbs.items():
            print(f'== {k}: {v}')
        print(f'=====================')

    # Save the player and world status
    def save(self):
        playerSaves = len(glob.glob1('saves/', 'Player*.json'))
        worldSaves = len(glob.glob1('saves/', 'World*.json'))

        # Create the Player save file
        playerData = self.player.toJSON()
        fn = f'saves/Player_{playerSaves+1}.json'
        with open(fn, 'w') as s:
            json.dump(playerData, s)
        print(f'Player saved as {fn}')

        # Create the World save file
        fn = f'saves/World_{worldSaves+1}.json'
        with open(fn, 'w') as s:
            json.dump(self.map, s)
        print(f'World saved as {fn}')

    # Quit the game
    def quit(self):
        if not questionYesNo('Are you sure you want to quit?'):
            return False
        if questionYesNo('Quitting...\nWould you like to save?'):
            self.save()
        self.isOver = True
        return True
