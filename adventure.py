'''
@title Text Adventure
@author Carlos Barcelos
@date TODO

The main class to start the adventure
'''

import os       # Search files/directories
import argparse # Command line arguments
import json     # Handle JSON files
import sys      # DEV TOOL

from src.Achievements import Achievements # Import the Achievements class
from src.GameEngine import GameEngine     # Import the GameEngine class
from src.Player import Player             # Import the Player class
from src.Map import Map             # Import the Map class
import src.stdlib as std                  # Import standard libraries

# Display the one-time, intro sequence to the game
def introSequence():
    print('            _____   __      __  ______   _   _   _______   _    _   _____    ______ ')
    print('    /\     |  __ \  \ \    / / |  ____| | \ | | |__   __| | |  | | |  __ \  |  ____|')
    print('   /  \    | |  | |  \ \  / /  | |__    |  \| |    | |    | |  | | | |__) | | |__   ')
    print('  / /\ \   | |  | |   \ \/ /   |  __|   |   ` |    | |    | |  | | |  _  /  |  __|  ')
    print(' / ____ \  | |__| |    \  /    | |____  | |\  |    | |    | |__| | | | \ \  | |____ ')
    print('/_/    \_\ |_____/      \/     |______| |_| \_|    |_|     \____/  |_|  \_\ |______|\n')

    # Get the player name
    pName = input('Welcome adventurer. What shall I call you? ')

    # Display classes to user and get the player class
    pClasses = {'Brute' : 'A bullheaded fighter with lots of strength but no tactical defense.',
    'Scholar' : 'An intelligent master of the books; saved little time for strength training.',
    'Defender' : 'A defensive master with average strength and little time for intellect.'}

    body = []
    for k, v in pClasses.items():
        body.append(f'{k}: {v}')
    std.prettyPrint('Class Selection', body)
    pClass = std.optionParse('Select your class:', list(pClasses.keys()))

    return (pName, pClass)

# Display the one-time, outro sequence to the game
def outroSequence():
    print('  _____                                 ____                        ')
    print(' / ____|                               / __ \                       ')
    print('| |  __    __ _   _ __ ___     ___    | |  | | __   __   ___   _ __ ')
    print('| | |_ |  / _  | |  _   _ \   / _ \   | |  | | \ \ / /  / _ \ |  __|')
    print('| |__| | | (_| | | | | | | | |  __/   | |__| |  \ V /  |  __/ | |   ')
    print(' \_____|  \__,_| |_| |_| |_|  \___|    \____/    \_/    \___| |_|   ')

# Initialize a new GameEngine with a game world and a player
def initalize(args):
    # Get the map
    fn = f'saves/{args.mapSave}.json'
    if args.mapSave and os.path.isfile(fn):
        with open(fn) as f:
            m = Map(json.load(f))
        print(f'Map loaded from {fn}')
    else:
        with open('saves/map.json') as f:
            m = Map(json.load(f))
    startingRoom = 'start'

    # Get the player
    fn = f'saves/{args.playerSave}.json'
    if args.playerSave and os.path.isfile(fn):
        # Read in the JSON data
        with open(fn) as f:
            pJSON = json.load(f)
        # Create a new player with the data
        p = Player(pJSON['pName'], pJSON['pClass'], pJSON['abilities'], pJSON['inventory'], pJSON['equipment'], \
            pJSON['level'], pJSON['hp'], pJSON['exp'], pJSON['expRate'], pJSON['gold'], pJSON['goldRate'], \
            pJSON['upgradesAvailable'], pJSON['stats'])
        startingRoom = pJSON['location']
        print(f'Player loaded from {fn}')
    else:
        pDetails = introSequence()
        p = Player(pDetails[0], pDetails[1])

    # Get the achievements
    fn = f'saves/{args.achievementSave}.json'
    if args.achievementSave and os.path.isfile(fn):
        with open(fn) as f:
            aJSON = json.load(f)
        print(f'Achievement loaded from {fn}')
    else:
        with open('saves/achievements.json') as f:
            aJSON = json.load(f)
    a = Achievements(aJSON)

    # Build the resources/lookup tables that the game needs
    r = {}
    with open('resources/items.json') as f:
        r['items'] = json.load(f)
    with open('resources/equipment.json') as f:
        r['equipment'] = json.load(f)
    with open('resources/story.json') as f:
        r['story'] = json.load(f)

    return GameEngine(m, p, a, r, startingRoom)

###############
## Main Loop ##
###############
def main(args):
    ge = initalize(args)

    # Start the core game loop
    while(not ge.isOver):
        ge.prompt()
        ge.achievements.checkAll(ge)

    outroSequence()
    return 0
##############
## End Main ##
##############

#########################
## Command-Line Inputs ##
#########################
parser = argparse.ArgumentParser(description='Adventure (Working Title)')

parser.add_argument('--map', dest='mapSave', type=str, default='',
                    help='The save file for the world')
parser.add_argument('--player', dest='playerSave', type=str, default='',
                    help='The save file for the player. Type only the file name, without extension. Ex) Player_1')
parser.add_argument('--achievement', dest='achievementSave', type=str, default='',
                    help='The achievements to use for this game')

args = parser.parse_args()
##############################
## End Command-Line Inputs ##
#############################

# Run Main
if __name__ == '__main__':
    main(args)
