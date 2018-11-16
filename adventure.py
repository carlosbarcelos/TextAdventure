'''
@title Text Adventure
@author Carlos Barcelos
@date TODO
'''

import sys      # Various system variables
import json     # Handle JSON files
import networkx as nx # Directed graph
import argparse # Command line arguments

from src.GameEngine import GameEngine # Import the GameEngine class
from src.Player import Player   # Import the Player class

# Display the one-time, intro sequence to the game
def introSequence():
    print('            _____   __      __  ______   _   _   _______   _    _   _____    ______ ')
    print('    /\     |  __ \  \ \    / / |  ____| | \ | | |__   __| | |  | | |  __ \  |  ____|')
    print('   /  \    | |  | |  \ \  / /  | |__    |  \| |    | |    | |  | | | |__) | | |__   ')
    print('  / /\ \   | |  | |   \ \/ /   |  __|   | . ` |    | |    | |  | | |  _  /  |  __|  ')
    print(' / ____ \  | |__| |    \  /    | |____  | |\  |    | |    | |__| | | | \ \  | |____ ')
    print('/_/    \_\ |_____/      \/     |______| |_| \_|    |_|     \____/  |_|  \_\ |______|\n')


    pName = input('Welcome adventurer. What shall I call you? ')

    pClasses = ['Brute', 'Scholar', 'Druid']
    pClass = 'NA'
    while pClass not in pClasses:
        pClass = input(f'Please select a class: {pClasses} > ')
    return Player(pName, pClass)

mapGraph = nx.DiGraph()

# Generate a human-readable graph from the map.json file
def generateMapGraph(map):
    global mapGraph

    # Make a directed graph structure from the map JSON
    mapGraph.add_nodes_from(map['Map'].keys())
    for room in mapGraph.nodes():
        for dest in map['Map'][room]['Connections'].values():
            mapGraph.add_edge(room, dest)

    # Pretty print the graph
    # TODO:

    print(mapGraph.nodes())
    print(mapGraph.edges())

###############
## Main Loop ##
###############
def main(args):
    # Initilization
    with open(args.worldSave) as f:
        m = json.load(f)
    # If there is a player save try that, else start the game manually
    if args.playerSave:
        with open(args.playerSave) as f:
            pJSON = json.load(f)
        # TODO: enable this
        # p = Player.createFromJSON(pJSON)
    else:
        #p = introSequence()
        p = Player('MyName', 'Brute') # Dev mode

    ge = GameEngine(m, p)
    # Start the core game loop
    while(not ge.isOver):
        ge.prompt()

    print('The adventure is over . . .')
    return 0

##############
## End Main ##
##############

#########################
## Command-Line Inputs ##
#########################
parser = argparse.ArgumentParser(description='Adventure (Working Title)')

parser.add_argument('--world', dest='worldSave', type=str, default='resources/map.json',
                    help='The save file for the world')
parser.add_argument('--player', dest='playerSave', type=str, default='',
                    help='The save file for the player')

args = parser.parse_args()
##############################
## End Command-Line Inputs ##
#############################

# Run Main
if __name__ == '__main__':
    main(args)
