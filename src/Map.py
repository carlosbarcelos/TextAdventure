'''
@title Text Adventure: Map Class
@author Carlos Barcelos
@date TODO

The map class with member veriables and functions.
'''

import math              # Math functionality

import src.stdlib as std # Import standard libraries
from src.Room import Room  # Import Room objects

class Map():
    def __init__(self, mapJSON, resources):
        self.rooms = toMap(mapJSON, resources)

    # Move a certain direction from the current room
    def move(self, thisRoom, dir):
        # Requested move is invalid
        if dir not in self.rooms[thisRoom].connections.keys():
            print(f"Move '{dir}': Invalid direction.")
            print(f"Possible directions from {thisRoom}: {self.rooms[thisRoom].connections}")
            return None, False
        else:
            # Record the move to the next room
            nextRoom = self.rooms[thisRoom].connections[dir]
            isNew = self.rooms[nextRoom].visited == 'False'
            self.rooms[nextRoom].visited = 'True'

            return nextRoom, isNew

    # Look around and get a feel for where you are
    def look(self, thisRoom):
        body = []

        body.append(self.rooms[thisRoom].description)
        body.append('')

        # Display connection information
        connList = self.rooms[thisRoom].connections
        if connList:
            body.append(f'There are a few connections from this room:')
            for k, v in connList.items():
                body.append(f'  To the {k.capitalize()} is {v.capitalize()}')
        else:
            body.append('There are no connections in this room.')

        # Display enemy information
        enemyList = self.rooms[thisRoom].enemies
        if enemyList:
            body.append('')
            enemyNames = [e.name for e in enemyList]
            enemyDescriptions = [e.description for e in enemyList]
            body.append(f'There are a few enemies here:')
            for k, v in zip(enemyNames, enemyDescriptions):
                body.append(f'  {k} : {v}')

        std.prettyPrint(self.rooms[thisRoom].title, body)
        return True

    # Examine an object on the map
    def examineObject(self, thisRoom, object):
        for o in self.rooms[thisRoom].examine:
            if o == object:
                description = self.rooms[thisRoom].examine[o]
                std.prettyPrint(object.capitalize(), [description])
                return True
        return False

    # Examine an enemy on the map
    def examineEnemy(self, thisRoom, object):
        for e in self.rooms[thisRoom].enemies:
            if e.name == object:
                description = e.description
                std.prettyPrint(object.capitalize(), [description])
                return True
        return False

    # Helper: Unlock a room connection
    def unlockAction(self, thisRoom, thatRoom, dir):
        self.rooms[thisRoom].connections[dir] = thatRoom
        self.rooms[thatRoom].connections[std.getOppDir(dir)] = thisRoom
        print('New room connection discovered.')

    # Helper: Spawn a new item in the room
    def spawnAction(self, thisRoom, items, resources):
        newItems = []

        for i in items:
            iObject = std.itemNameToObject(i, resources)
            self.rooms[thisRoom].items.append(iObject)
            newItems.append(iObject.name)

        if newItems: print(f'New items were added to the room: {newItems}')

    # Display the map; Expects a square map
    # TODO Highlight the current room on the map
    def displayMap(self, options, player):
        # Initalize data structures
        mapLen = int(math.sqrt(len(self.rooms.keys())))
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
        for room in self.rooms.values():
            roomCoord = room.coordinates
            roomIcon = room.icon
            # If the player has the area map, display the icon
            if player.inInventory(f"{room.area} Area Map"):
                mapArr[roomCoord[0]][roomCoord[1]] = roomIcon
            # If this is an empty room, display filled in icon
            elif room.title == 'empty':
                mapArr[roomCoord[0]][roomCoord[1]] = '#'
            # Else, display a fog
            else:
                mapArr[roomCoord[0]][roomCoord[1]] = '~'

            # If this room has connections, note them on the map
            connections = room.connections.keys()
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
        return self.rooms[thisRoom].icon == 'S'

    # Convert from a map object to a JSON string
    def toJSON(self):
        jData = {}
        for k, v in self.rooms.items():
            jData[k] = v.toJSON()
        return jData

# Convert from a JSON string to an map object
def toMap(mapJSON, resources):
    # Add the explicity rooms
    map = {}
    for name, details in mapJSON.items():
        map[name] = Room(name, details, resources)


    # Find the coordinates of the implicit, empty rooms
    filledCoords = []
    maxX = 0
    maxY = 0
    for roomName in map:
        coord = map[roomName].coordinates
        if coord[0] > maxX: maxX = coord[0] # Find the maximum X coordinate
        if coord[1] > maxY: maxY = coord[1] # Find the maximum Y coordinate
        filledCoords.append(coord)

    # Add the implicit, empty rooms
    emptyDesc = {'title':'empty','description':'empty','connections':{},'area':'empty','icon':'|||','coordinates':[],'visited':True}
    for i in range(maxX+1):
        for j in range(maxY+1):
            if [i,j] not in filledCoords:
                emptyDesc['coordinates'] = [i,j]
                map[f'empty_{i}_{j}'] = Room('empty', emptyDesc, resources)

    return map
