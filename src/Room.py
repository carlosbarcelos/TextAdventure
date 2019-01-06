'''
@title Text Adventure: Room Class
@author Carlos Barcelos
@date 06 January 2019

The room class with member veriables and functions.
'''

import src.stdlib as std            # Import standard libraries
from src.Item import Item           # Work with Item objects
from src.Enemy import Enemy           # Work with Item objects
from src.Equipment import Equipment # Work with Equipment objects

class Room():
    def __init__(self, name, details, resources):
        self.name = name
        room = toRoom(details, resources)
        self.title = room['title']
        self.description = room['description']
        self.items = room['items']
        self.examine = room['examine']
        self.use = room['use']
        self.enemies = room['enemies']
        self.connections = room['connections']
        self.area = room['area']
        self.icon = room['icon']
        self.coordinates = room['coordinates']
        self.visited = room['visited']

    # Overload __str__
    def __str__(self):
        return str(self.name)

    # Convert from a room object to a JSON string
    def toJSON(self):
        jData = {}
        jData['title'] = self.title
        jData['description'] = self.description
        jData['items'] = []
        for item in self.items:
            i = item.dictName
            jData['items'].append(i)
        jData['examine'] = self.examine
        jData['use'] = self.use
        jData['enemies'] = []
        for enemy in self.enemies:
            e = enemy.toJSON()
            jData['enemies'].append(e)
        jData['connections'] = self.connections
        jData['area'] = self.area
        jData['icon'] = self.icon
        jData['coordinates'] = self.coordinates
        jData['visited'] = self.visited
        return jData

# Convert from a JSON string to a room object
def toRoom(details, resources):
    room = {}
    room['title'] = details['title']
    room['description'] = details['description']
    room['items'] = []
    for item in details['items']:
        i = std.itemNameToObject(item, resources)
        room['items'].append(i)
    room['examine'] = details['examine']
    room['use'] = details['use']
    room['enemies'] = []
    for eDetails in details['enemies']:
        e = Enemy(eDetails['name'], eDetails, resources)
        room['enemies'].append(e)
    room['connections'] = details['connections']
    room['area'] = details['area']
    room['icon'] = details['icon']
    room['coordinates'] = details['coordinates']
    room['visited'] = details['visited']
    return room
