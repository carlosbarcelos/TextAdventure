'''
@title Text Adventure: GameEngine Class
@author Carlos Barcelos
@date TODO

The GameEngine class with member veriables and functions.
'''

import glob                   # Search files/directories
import json                   # Handle JSON files
import math                   # Math functionality
from datetime import datetime # Current datetime

BATTLE_EXP = 10
EXPLORE_EXP = 5
TBD_DEF_EXP = 5

# Provide a user propt with a given question and acceptible responses
def optionParse(question, answers):
    while "invalid response":
        prettyAnswers = ' ('
        for i in range(len(answers)):
            prettyAnswers += str(answers[i])
            if not i == len(answers)-1:
                prettyAnswers += '/'

        reply = str(input(question+prettyAnswers+')> '))
        if reply in answers:
            return reply

class GameEngine():
    def __init__(self, map, player, achievements, resources):
        self.map = map
        self.player = player
        self.achievements = achievements
        self.resources = resources
        self.currentRoom = 'Room 1' # TODO Make this dynamic
        self.isOver = False
        self.verbs = {
        'help' : '[]',
        'look' : 'Examine your surroundings',
        'move' : '[dir] Determine the direction in which to travel',
        'take' : '[item] Take an item found in the world',
        'use' : '[item] Performs an action with a given item',
        'equip': '[equipment] Equip a piece of equipment',
        'unequip': '[equipment] Unequip a piece of equipment',
        'battle' : '[enemy] Initiate a battle with an enemy',
        'map' : 'Display the map with a legend',
        'read' : '[log] Read a given story log',
        'stats' : 'Print the player stats',
        'inventory' : 'Print the player inventory : [-l] Long print, include description',
        'equipment' : 'Print the player equipment',
        'upgrade' : 'Upgrade the player stats',
        'achievements' : 'Get the current achievement progress',
        'save' : 'Save progress [Only allowed in designated areas]',
        'quit' : 'Quit the game'}

    # Promt the user for action
    def prompt(self):
        newInput = input(f'{self.currentRoom} > ').strip()
        self.parse(newInput)

    # Get the action word and additional options
    def parse(self, inStr):
        returnState = False
        returnDict = {'verb': None, 'noun': None, 'option': ['']}
        words = inStr.split()

        # Reject empty strings
        if inStr:
            # Accept maximum one word after verb
            if len(words) == 1:
                returnDict['verb'] = words[0]
            elif len(words) >= 2:
                returnDict['verb'] = words[0]
                returnDict['noun'] = words[1]
                returnDict['option'] = words[2:]
            returnState = self.workInputOptions(returnDict['verb'], returnDict['noun'], returnDict['option'])
        return returnState

    # Work on input and additional options
    def workInputOptions(self, verb, noun, options):
        if not verb in self.verbs.keys():
            return False

        switcher = {
            'help': lambda: self.help(),
            'look' : lambda: self.look(),
            'move': lambda: self.move(noun),
            'take': lambda: self.take(noun),
            'use': lambda: self.use(noun),
            'equip': lambda: self.player.equip(noun, options),
            'unequip': lambda: self.player.unequip(noun, options),
            'battle': lambda: self.battle(noun),
            'map': lambda: self.displayMap(),
            'read': lambda: self.readStory(noun, options),
            'stats': lambda: self.player.printStats(),
            'inventory': lambda: self.player.printInventory(options),
            'equipment': lambda: self.player.printEquipment(options),
            'upgrade': lambda: self.player.upgrade(),
            'achievements' : lambda: self.achievements.reportAll(),
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

        # Requested move is valid
        try:
            nextRoom = self.map[self.currentRoom]['Connections'][dir]
            self.currentRoom = self.map[nextRoom]['Title']
            # Given Exp and print description if this is a new room
            if self.map[self.currentRoom]['Visited'] == 'False':
                self.player.getExp(EXPLORE_EXP)
                self.look()
                self.map[self.currentRoom]['Visited'] = 'True'
            return True
        # Requested move is invalid
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
            self.player.getItems([noun], self.resources)
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
                    self.player.getExp(BATTLE_EXP)
                    if e['Inventory']:
                        self.player.getItems(e['Inventory'], self.resources)
                    self.map[self.currentRoom]['Enemies'].remove(e)
                    return True

                else:
                    # The enemy hits the player
                    self.player.hp -= e['Damage']
                    print(f"You lost that battle. {e['Name']} hit you for {e['Damage']} HP.")

                    # Check that the player is still alive
                    if not self.player.isAlive():
                        print('That was the last of your HP. Your adventure is over.')
                        self.isOver = True
                    return False

        print(f"The enemy '{noun}' is not in this room")
        return None

    # Display the map; Expects a square map
    def displayMap(self):
        # Initalize data structures
        mapLen = int(math.sqrt(len(self.map.keys())))
        mapArr = [[' ' for x in range(mapLen)] for y in range(mapLen)]
        eastConn = [[' ' for x in range(mapLen)] for y in range(mapLen)]
        southConn = [[' ' for x in range(mapLen)] for y in range(mapLen)]

        # Create 2D map and border arrays
        for room in self.map.values():
            roomCoord = room['Coordinates']
            roomIcon = room['Icon']
            # If the player has the area map, display the icon
            if f"{room['Area']} Map" in self.player.inventory:
                mapArr[roomCoord[0]][roomCoord[1]] = roomIcon
            # Else, display a fog
            else:
                mapArr[roomCoord[0]][roomCoord[1]] = '~'

            # If this room has connections, note them on the map
            connections = room['Connections'].keys()
            strVal =  ' '
            if 'east' not in connections:
                strVal =  '|'
            eastConn[roomCoord[0]][roomCoord[1]] = strVal

            strVal =  '   +'
            if 'south' not in connections:
                strVal = '---+'
            southConn[roomCoord[0]][roomCoord[1]] = strVal

        # Piece together the map and display
        print('+' + ('---+'*len(mapArr)))
        for i in range(len(mapArr)):
            # Print the rooom information
            rowStr = '|'
            for j in range(len(mapArr[i])):
                rowStr += f' {mapArr[i][j]} {eastConn[i][j]}'
            print(rowStr)

            # Print the divider information
            dividerStr = '+'
            for d in southConn[i]:
                dividerStr += d
            print(dividerStr)

    # Read a given story log
    def readStory(self, noun, options):
        if noun is None:
            print('Please specify a story log.')
            return False

        log = noun + ' ' + ' '.join(options)

        # The player must have the story log to read it
        for i in self.player.inventory:
            if str(i) == log:
                textWidth = 40
                print(f"/{textWidth*'~'}/")
                for l in i.text:
                    padding = textWidth - len(l)
                    print(f"/ {l}{(padding-1)*' '}/")
                print(f"/{textWidth*'~'}/")
                return True
        print('You do not have access to that story log.')
        return False


    # Look around and get a feel for where you are
    def look(self):
        print(self.map[self.currentRoom]['Description'])

        # Display connection information
        connList = self.map[self.currentRoom]['Connections']
        if connList:
            print(f'There are a few connections from this room: {connList}')
        else:
            print('There are no connections in this room.')

        # Display enemy information
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

    # Save the game and replenish the player health. Only allowed in save rooms
    def save(self):
        if not self.map[self.currentRoom]['Icon'] == 'S':
            print('The save feature is only allowed in designated areas.')
            return False

        playerSaves = len(glob.glob1('saves/', 'Player*.json'))
        worldSaves = len(glob.glob1('saves/', 'World*.json'))

        # Replenish health
        self.player.hp = self.player.MAX_HP

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
        if 'n' == optionParse('Are you sure you want to quit?', ['y','n']):
            return False
        # TODO Should save be allowed on quit?
        # print('Quitting...')
        # if 'y' == optionParse('Would you like to save?', ['y','n']):
        #     self.save()
        self.isOver = True
        return True
