'''
@title Text Adventure: GameEngine Class
@author Carlos Barcelos
@date TODO

The GameEngine class with member veriables and functions.
'''

import glob                     # Search files/directories
import json                     # Handle JSON files
from datetime import datetime   # Current datetime
import src.stdlib as std        # Import standard libraries

BATTLE_EXP = 10
EXPLORE_EXP = 5
TBD_DEF_EXP = 5

class GameEngine():
    def __init__(self, map, player, achievements, resources, currentRoom):
        self.map = map
        self.player = player
        self.achievements = achievements
        self.resources = resources
        self.currentRoom = currentRoom
        self.isOver = False
        self.verbs = {
        'help' : 'Display this help information',
        'look' : 'Take in your surroundings',
        'examine' : 'Examine an object in the world',
        'move' : '[dir] Determine the direction in which to travel',
        'take' : '[item] Take an item found in the world',
        'use' : '[item] Performs an action with a given item',
        'equip': '[equipment] Equip a piece of equipment',
        'unequip': '[equipment] Unequip a piece of equipment',
        'battle' : '[enemy] Initiate a battle with an enemy',
        'map' : 'Display the map with a legend : [-l] Legend',
        'read' : '[log] Read a given story log',
        'stats' : 'Print the player stats',
        'inventory' : 'Print the player inventory : [-l] Long print',
        'equipment' : 'Print the player equipment : [-l] Long print',
        'upgrade' : 'Upgrade the player stats',
        'achievements' : 'Get the current achievement progress',
        'save' : 'Save progress [Only allowed in designated areas]',
        'quit' : 'Quit the game'}

    # Promt the user for action
    def prompt(self):
        newInput = input(f'\n{self.currentRoom} > ').lower().strip()
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
            'look' : lambda: self.map.look(self.currentRoom),
            'examine' : lambda: self.examine(noun, options),
            'move': lambda: self.move(noun),
            'take': lambda: self.take(noun, options),
            'use': lambda: self.use(noun, options),
            'equip': lambda: self.player.equip(noun, options),
            'unequip': lambda: self.player.unequip(noun, options),
            'battle': lambda: self.battle(noun),
            'map': lambda: self.map.displayMap(noun, self.player),
            'read': lambda: self.readStory(noun, options),
            'stats': lambda: self.player.printStats(),
            'inventory': lambda: self.player.printInventory(noun),
            'equipment': lambda: self.player.printEquipment(noun),
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

        nextRoom, isNew = self.map.move(self.currentRoom, dir)
        # Make the move
        if nextRoom:
            self.currentRoom = nextRoom
        # Given Exp and print description if this is a new room
        if isNew:
            self.player.getExp(EXPLORE_EXP)
            self.map.look(self.currentRoom)

        return True

    # Taken a given item and add it to the player inventory
    def take(self, noun, options):
        if noun is None:
            print('Take requires a noun as input.')
            return False

        requestItem = (noun + ' ' + ' '.join(options)).strip()

        for i in self.map.map[self.currentRoom]['Items']:
            roomItem = std.itemNameToObject(i, self.resources)

            if requestItem == str(roomItem):
                self.map.map[self.currentRoom]['Items'].remove(i)
                self.player.getItems([i], self.resources)
                return True

        print(f'{requestItem} is not in the room.')
        return False

    # Use a given item
    # TODO Support more usable world items
    def use(self, noun, options):
        if noun is None:
            print('Must use a specific item.')
            return False

        item = (noun + ' ' + ' '.join(options)).strip()

        # Try to use the item from the world
        useStatus = False
        if item in self.map.map[self.currentRoom]['Use']:
            useStatus = self.useObject(item)
        if not useStatus:
            useStatus = self.useAbility(item)
        # Try to use the item from the player
        if not useStatus:
            useStatus = self.player.use(item)

        if not useStatus:
            print(f'You cannot use \'{item}\' at this time.')
        return useStatus

    # Helper: Use a given ability
    def useAbility(self, noun):
        useStatus = False
        abilities = [(k, v['name'].lower()) for k,v in self.player.abilities.items()]

        for k, v in abilities:
            # Does the player have the action?
            if v == noun:
                # Does the room support the action
                if f'ab_{k}' in self.map.map[self.currentRoom]['Use']:
                    # TODO Give abilities more use. Right now, just open doors
                    unlock = self.map.map[self.currentRoom]['Use'][f'ab_{k}']['unlock']
                    # Handle ATK relic
                    if k == 'atk':
                        self.map.unlockAction(self.currentRoom, unlock[1], unlock[0])
                    # Handle INT relic
                    if k == 'int':
                        self.map.unlockAction(self.currentRoom, unlock[1], unlock[0])
                    # Handle DEF relic
                    if k == 'def':
                        self.map.unlockAction(self.currentRoom, unlock[1], unlock[0])

                    # Actions are single use, remove from the map once used
                    del self.map.map[self.currentRoom]['Use'][f'ab_{k}']
                    useStatus = True

        return useStatus

    # Helper: Use an item from the world
    def useObject(self, item):
        returnStatus = False
        itemValue = self.map.map[self.currentRoom]['Use'][item]
        if item == 'button' or item == 'lever':
            print(itemValue['description'])
            # TODO Revisit buttons. Whhat else should they be able to do?
            for action in itemValue:
                if action == 'unlock':
                    self.map.unlockAction(self.currentRoom, itemValue[action][1], itemValue[action][0])
                elif action == 'spawn':
                    self.map.spawnAction(self.currentRoom, itemValue[action])
            # Actions are single use, remove from the map once used
            del self.map.map[self.currentRoom]['Use'][item]
            returnStatus = True
        elif item == 'chest' or item == 'crate':
            # Pretty print container contents to user
            itemValueNames = []
            for i in itemValue:
                itemValueNames.append(self.resources['items'][i]['name'])
            std.prettyPrint(item, itemValueNames)
            # The user can take all or none of the items in the container
            if 'y' == std.optionParse('Take all the items?', ['y','n']):
                self.player.getItems(itemValue, self.resources)
                # Actions are single use, remove from the map once used
                del self.map.map[self.currentRoom]['Use'][item]
                returnStatus = True
        else:
            print('Unexpected item.')

        return returnStatus

    # Battle an enemy in the room
    # TODO: Return the victor of the battle or None if no battle took place
    def battle(self, noun):
        # A battle cannot take place without an enemy
        if not self.map.map[self.currentRoom]['Enemies']:
            print('There are no enemies in this room to battle')
            return False

        # An enemy must be selected to start a battle
        if noun is None:
            print('Select an enemy to battle.')
            return False

        # Find the enemy in the room
        for e in self.map.map[self.currentRoom]['Enemies']:
            if e['Name'] == noun:
                # If the enemy has move than one stat, start topTrumpBattle()
                if len(e['Stats']) > 1:
                    isVictorious = self.player.topTrumpBattle(e)

                # Else, start a normal battle
                else:
                    [(eStat, eStatValue)] = e['Stats'].items()
                    isVictorious = self.player.battle(e, (eStat, eStatValue))

                # Perform after action report
                if isVictorious:
                    print('You won that battle.')
                    # Reward the player for victory
                    self.player.getExp(BATTLE_EXP)
                    if e['Inventory']:
                        self.player.getItems(e['Inventory'], self.resources)
                    self.map.map[self.currentRoom]['Enemies'].remove(e)
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
        return False

    # Read a given story log
    def readStory(self, noun, options):
        if noun is None:
            print('Please specify a story log.')
            return False

        log = (noun + ' ' + ' '.join(options)).strip()

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

    # Examine an object in the world
    def examine(self, noun, options):
        if noun is None:
            print('Please specify an object.')
            return False

        object = (noun + ' ' + ' '.join(options)).strip()

        examineSuccess = False
        # 1) Examine objects in the room (if they are there)
        if not examineSuccess:
            examineSuccess = self.map.examineObject(self.currentRoom, object)
        # 2) Examine enemies in the room
        if not examineSuccess:
            examineSuccess = self.map.examineEnemy(self.currentRoom, object)
        # 3) Examine objects in the player inventory
        if not examineSuccess:
            for i in self.player.inventory:
                if i.name == object:
                    description = i.description
                    std.prettyPrint(object.capitalize(), [description])
                    examineSuccess =  True
        return examineSuccess

    # Display help information
    def help(self):
        # Get the printable text
        body = []
        for k, v in self.verbs.items():
            body.append(f'{k}: {v}')

        # Hand off the print to the helper
        std.prettyPrint('HELP', body)
        return True

    # Save the game and replenish the player health. Only allowed in save rooms
    def save(self):
        if not self.map.isSaveRoom(self.currentRoom):
            print('The save feature is only allowed in designated areas.')
            return False

        playerSaves = len(glob.glob1('saves/', 'Player*.json'))
        worldSaves = len(glob.glob1('saves/', 'World*.json'))

        # Replenish health
        self.player.hp = self.player.MAX_HP

        # Create the Player save file
        playerData = self.player.toJSON(self.currentRoom)
        fn = f'saves/Player_{playerSaves+1}.json'
        with open(fn, 'w') as s:
            json.dump(playerData, s)
        print(f'Player saved as {fn}')

        # Create the World save file
        fn = f'saves/World_{worldSaves+1}.json'
        with open(fn, 'w') as s:
            json.dump(self.map.map, s)
        print(f'World saved as {fn}')

    # Quit the game
    def quit(self):
        if 'n' == std.optionParse('Are you sure you want to quit?', ['y','n']):
            return False
        # TODO Should save be allowed on quit?
        # print('Quitting...')
        # if 'y' == std.optionParse('Would you like to save?', ['y','n']):
        #     self.save()
        self.isOver = True
        return True
