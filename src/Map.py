'''
@title Text Adventure: Map Class
@author Carlos Barcelos
@date TODO

The map class with member veriables and functions.
'''

import math                     # Math functionality

import src.stdlib as std        # Import standard libraries

class Map():
    def __init__(self, mapJSON):
        self.map = mapJSON

    # Move a certain direction from the current room
    def move(self, thisRoom, dir):
        # Requested move is invalid
        if dir not in self.map[thisRoom]['Connections'].keys():
            print(f"Move '{dir}': Invalid direction.")
            print(f"Possible directions from {thisRoom}: {self.map[thisRoom]['Connections']}")
            return None, False
        else:
            # Record the move to the next room
            nextRoom = self.map[thisRoom]['Connections'][dir]
            isNew = self.map[nextRoom]['Visited'] == 'False'
            self.map[nextRoom]['Visited'] = 'True'

            return nextRoom, isNew

    # Look around and get a feel for where you are
    def look(self, thisRoom):
        body = []

        body.append(self.map[thisRoom]['Description'])
        body.append('')

        # Display connection information
        connList = self.map[thisRoom]['Connections']
        if connList:
            body.append(f'There are a few connections from this room:')
            for k, v in connList.items():
                body.append(f'  To the {k.capitalize()} is {v.capitalize()}')
        else:
            body.append('There are no connections in this room.')

        # Display enemy information
        enemyList = self.map[thisRoom]['Enemies']
        if enemyList:
            body.append('')
            enemyNames = [e['Name'] for e in enemyList]
            enemyDescriptions = [e['Description'] for e in enemyList]
            body.append(f'There are a few enemies here:')
            for k, v in zip(enemyNames, enemyDescriptions):
                body.append(f'  {k} : {v}')

        std.prettyPrint(self.map[thisRoom]['Title'], body)
        return True

    # Examine an object on the map
    def examineObject(self, thisRoom, object):
        for o in self.map[thisRoom]['Examine']:
            if o == object:
                description = self.map[thisRoom]['Examine'][o]
                std.prettyPrint(object.capitalize(), [description])
                return True
        return False

    # Examine an enemy on the map
    def examineEnemy(self, thisRoom, object):
        for e in self.map[thisRoom]['Enemies']:
            if e['Name'] == object:
                description = e['Description']
                std.prettyPrint(object.capitalize(), [description])
                return True
        return False

    # Helper: Unlock a room connection
    def unlockAction(self, thisRoom, thatRoom, dir):
        self.map[thisRoom]["Connections"][dir] = thatRoom
        self.map[thatRoom]["Connections"][std.getOppDir(dir)] = thisRoom
        print('New room connection discovered.')

    # Helper: Spawn a new item in the room
    def spawnAction(self, thisRoom, items):
        itemsAdded = False
        for i in items:
            self.map[thisRoom]['Items'].append(i)
            itemsAdded = True
        if itemsAdded: print('New items were added to the room.')

    # Display the map; Expects a square map
    # TODO Highlight the current room on the map
    def displayMap(self, options, player):
        # Initalize data structures
        mapLen = int(math.sqrt(len(self.map.keys())))
        mapArr = [[' ' for x in range(mapLen)] for y in range(mapLen)]
        eastConn = [[' ' for x in range(mapLen)] for y in range(mapLen)]
        southConn = [[' ' for x in range(mapLen)] for y in range(mapLen)]

        # (Optionally) Print the legend
        if options == '-l':
            body = []
            body.append('S : Save Room')
            body.append('~ : Hidden')
            std.prettyPrint('Map Legend', body)

        # Create 2D map and border arrays
        for room in self.map.values():
            roomCoord = room['Coordinates']
            roomIcon = room['Icon']
            # If the player has the area map, display the icon
            if player.inInventory(f"{room['Area']} Area Map"):
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

        return True

    # Determine if this is a save room
    def isSaveRoom(self, thisRoom):
        return self.map[thisRoom]['Icon'] == 'S'
