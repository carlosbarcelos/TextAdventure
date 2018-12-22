'''
@title Text Adventure: Player Class
@author Carlos Barcelos
@date TODO

The player class with member veriables and functions.
'''

from random import randint # Pseudo-random numbers

import src.stdlib as std            # Import standard libraries
from src.Item import Item           # Work with Item objects
from src.Story import Story         # Work with Story objects
from src.Equipment import Equipment # Work with Equipment objects

MAX_EXP = 100
MIN_STAT_UP = 4
MAX_STAT_UP = 5
MAX_STAT_VAL = 100

eqStructure={"head":"", "chest":"", "legs":"","necklace":"", "ring":"", "staff":""} # Equipment dictionary structure
stStructure={"atk":0, "int":0, "def":0} # Stats dictionary structure

# Set the player stats based on their selected class
def setPlayerStats(pClass):
    # atk Class
    if pClass == 'brute':
        stats = {'atk' : [10, 20], 'int' : [5, 10], 'def' : [0, 5]}
    # int Class
    elif pClass == 'scholar':
        stats = {'atk' : [0, 5], 'int' : [10, 20], 'def' : [5, 10]}
    # def Class
    elif pClass == 'defender':
        stats = {'atk' : [5, 10], 'int' : [0, 5], 'def' : [10, 20]}
    return stats

class Player():
    def __init__(self, pName, pClass, inventory=[], equipment=eqStructure, level=1, hp=99, exp=0, expRate=1, gold=0, goldRate=1, upgradesAvailable=0, stats=stStructure):
        self.pName = pName
        self.pClass = pClass
        self.inventory = inventory
        self.equipment = equipment
        self.level = level
        self.hp = hp
        self.MAX_HP = 90 + (self.level * 9)
        self.exp = exp
        self.expRate = expRate
        self.gold = gold
        self.goldRate = goldRate
        self.upgradesAvailable = upgradesAvailable
        self.stats = setPlayerStats(self.pClass) # TODO Fix this to work with saves

    # Print the player stats
    def printStats(self):
        header = f'{self.pName} the {self.pClass.capitalize()}'

        # Get the printable text
        body = []
        if self.upgradesAvailable:
            body.append(f'Lvl ({self.upgradesAvailable}): {self.level}')
        else:
            body.append(f'Lvl: {self.level}')
        body.append(f'Exp: {self.exp} / {MAX_EXP}')
        body.append('')
        body.append(f'HP: {self.hp} / {self.MAX_HP}')
        body.append(f'Gold: {self.gold}')
        body.append('')
        body.append(f"ATK: {self.stats['atk'][0]}..{self.stats['atk'][1]}")
        body.append(f"INT: {self.stats['int'][0]}..{self.stats['int'][1]}")
        body.append(f"DEF: {self.stats['def'][0]}..{self.stats['def'][1]}")

        # Hand off the print to the helper
        std.prettyPrint(header, body)

    # Print the player inventory
    def printInventory(self, options):
        if not self.inventory:
            print('Your inventory is empty.')
            return False

        # Get the printable text
        body = []
        for i in self.inventory:
            # Get the count of items
            count = ''
            if hasattr(i, 'count'):
                if i.count > 1:
                    count = f'({i.count}) '

            if options == '-l': # Long print description
                body.append(f'{count}{i.name}: {i.description}')
            else:
                body.append(f'{count}{i.name}')

        # Hand off the print to the helper
        std.prettyPrint('INVENTORY', body)

    # Print the player equipment list
    def printEquipment(self, options):
        if not ''.join([str(e) for e in self.equipment.values()]):
            print('You are not wearing any equipment.')
            return False

        # Get the printable text
        body = []
        for pos, e in self.equipment.items():
            if e:
                if options == '-l': # Long print description
                    body.append(f'[{pos}] {e.name}: {e.description}')
                else:
                    body.append(f'[{pos}] {e.name}')

        # Hand off the print to the helper
        std.prettyPrint('EQUIPMENT', body)

    # Gain additional Exp
    def getExp(self, val):
        print(f'+{val} Exp')
        val = int(round(val * self.expRate)) # Apply Exp rate
        prevLevel = self.level
        self.level += (self.exp + val) // MAX_EXP
        self.upgradesAvailable += (self.exp + val) // MAX_EXP
        self.exp = (self.exp + val) % MAX_EXP
        # Handle level up
        if self.level > prevLevel:
            self.hp = self.MAX_HP
            print('Level Up!')
        return True

    # Gain additional HP
    def getHp(self, val):
        hpApplied = False
        # Apply HP if not full
        if not self.hp == self.MAX_HP:
            # Do not give more than MAX_HP
            if self.hp + val > self.MAX_HP:
                hpToApply = self.MAX_HP - self.hp
            else:
                hpToApply = val
            self.hp += hpToApply
            print(f'+{hpToApply} HP')
            hpApplied = True
        else:
            print('HP already at full')
        return hpApplied

    # Gain additional gold
    def getGold(self, val):
        val += int(round(self.goldRate)) # Apply gold rate
        self.gold += val

    # Trade in one level for for one stat upgrade
    def upgrade(self):
        if self.upgradesAvailable < 1:
            print('You have no upgrades available.')
            return False

        # Prompt which stat to upgrade
        availableStats = []
        for s in ['atk', 'int', 'def']:
            if self.stats[s][0] != MAX_STAT_VAL and self.stats[s][1] != MAX_STAT_VAL:
                availableStats.append(s)

        if not availableStats:
            print('There are no stats available to upgrade.')
            return False

        selectedStat = std.optionParse('Select a stat to upgrade:', availableStats)

        # Prompt which attribute to upgrade
        availableAttr = []
        # MIN value cannot be larger than MAX
        if (self.stats[selectedStat][0]+MIN_STAT_UP) < self.stats[selectedStat][1]:
            availableAttr.append('MIN')
        # MAX value cannot be larger than MAX_STAT_VAL
        if (self.stats[selectedStat][1]+MAX_STAT_UP) < MAX_STAT_VAL:
            availableAttr.append('MAX')

        if not availableAttr:
            print(f'There are no attributes available to upgrade for {selectedStat}')
            return False

        selectedAttr = std.optionParse('Select an attribute to upgrade', availableAttr)

        # Do the upgrade and report to user
        upgradePos = 0 if (selectedAttr=='MIN') else 1
        upgradeVal = MIN_STAT_UP if (selectedAttr=='MIN') else MAX_STAT_UP
        self.stats[selectedStat][upgradePos] += upgradeVal
        self.upgradesAvailable -= 1
        print(f'Successfully upgraded {selectedAttr} attribute of {selectedStat} stat.')
        return True

    # Add items to the player inventory
    def getItems(self, items, resources):
        returnValue = False
        for i in items:
            iObject = std.itemNameToObject(i, resources)
            if iObject:
                # If the item is already in the inventory, increase the count
                if self.inInventory(str(iObject)):
                    for pItem in self.inventory:
                        if str(iObject) == str(pItem):
                            pItem.count += 1
                else:
                    self.inventory.append(iObject)
                print(f'You got: {str(iObject)}')
                returnValue = True

        return returnValue

    # Use a given item
    def useItem(self, item):
        thisItem = None
        itemUsed = False
        # Get the Item object
        for i in self.inventory:
            if i.name == item:
                thisItem = i

        # Make sure the item is in the inventory
        if thisItem == None:
            print('You do not have access to that item.')
            return False

        # Make sure the item can be used
        try:
            if not thisItem.usable:
                print('That item is not usable.')
                return False
        except AttributeError:
            print('That item is not usable.')
            return False

        # Switch on supported items
        if thisItem.name == 'key':
            print('TODO key logic')
        elif thisItem.name == 'health potion':
            itemUsed = self.getHp(10)
        elif thisItem.name == 'experience gem':
            itemUsed = self.getExp(25)
        else:
            print('This item is not supported')
            return False

        # Consume a usable item if it was used
        if itemUsed:
            if thisItem.uses > 1:
                thisItem.uses -= 1
            # When this is the last use either decrease the item count or discard the item
            else:
                if thisItem.count > 1:
                    thisItem.count -= 1
                    thisItem.uses = thisItem.defaultUses
                else:
                    self.inventory.remove(thisItem)
                    print(f'You used the last of the {thisItem}')

        return True

    # Check the player inventory for a certain common name item of a certain quantity
    def inInventory(self, itemName, count=0):
        returnStatus = False
        for i in self.inventory:
            # Checj for item and count
            if count:
                if i.name == itemName and i.count == count:
                    returnStatus = True
                    break
            # No count given, check for item
            elif i.name == itemName:
                returnStatus = True
                break
        return returnStatus

    # Do battle with some enemy
    def battle(self, e, statTuple):
        # Enemy battle information
        statType = statTuple[0]
        eStatVal = statTuple[1]

        # Get the players battle value from within the range
        pStatVal = randint(self.stats[statType][0], self.stats[statType][1])

        # Prepare for pretty print
        body = []
        body.append(f'{self.pName}: {pStatVal}')
        body.append(f"{e['Name']}: {eStatVal}")
        std.prettyPrint(f'{statType} Battle', body)

        return pStatVal > eStatVal

    # Start a 'top trumps' battle with an enemy
    def topTrumpBattle(self, e):
        eStats = list(e['Stats'].keys())

        # Report the stats comparison
        body = []
        body.append(f"{self.pName} vs. {e['Name']}")
        for s in eStats:
            pStatMin = self.stats[s][0]
            pStatMax = self.stats[s][1]
            eStat = e['Stats'][s]
            body.append(f'{s}: {pStatMin}..{pStatMax} vs. {eStat}')

        # Hand off the print to the helper
        std.prettyPrint('Stat Comparison', body)

        # Ask player which stat to battle
        selectedStat = std.optionParse('Select stat to use in battle:', eStats)

        # Get the enemy value and return the battle
        statTuple = (selectedStat, e['Stats'][selectedStat])
        return self.battle(e, statTuple)


    # Equip a piece of equipment
    def equip(self, noun, options):
        if noun is None:
            print('Equip requires a noun as input.')
            return False

        equipment = (noun + ' ' + ' '.join(options)).strip()

        # Move equipment from inventory to equipment slot
        for i in self.inventory:
            # Get the equipment
            if str(i) == equipment:
                # Make sure there is not already something in its spot
                pos = i.position
                if self.equipment[pos]:
                    print(f'There is already equipment in the {pos} slot.')
                    return False
                else:
                    # Do the move
                    self.inventory.remove(i)
                    self.equipment[pos] = i

                    # Apply status effects
                    # Secondary Equipment
                    if i.attribute in ['hp','expRate','goldRate']:
                        setattr(self, i.attribute, getattr(self, i.attribute) + i.value)
                    # Primary Equipment
                    else:
                        self.stats[i.attribute][0] += i.value
                        self.stats[i.attribute][1] += i.value
                    return True

        print('You do not have access to that piece of equipment.')
        return False

    # Unequip a piece of equipment
    def unequip(self, noun, options):
        if noun is None:
            print('Equip requires a noun as input.')
            return False

        equipment = noun + ' ' + ' '.join(options)

        # Move equipment from equipment slot to inventory
        for pos, e in self.equipment.items():
            if str(e) == equipment:
                # Remove status effects
                # Secondary Equipment
                if e.attribute in ['hp','expRate','goldRate']:
                    setattr(self, e.attribute, getattr(self, e.attribute) - e.value)
                # Primary Equipment
                else:
                    self.stats[e.attribute][0] -= e.value
                    self.stats[e.attribute][1] -= e.value

                # Do the move
                self.equipment[pos] = ''
                self.inventory.append(e)
                return True

        print('That piece of equipment is not equiped.')
        return False

    # Is the player still alive?
    def isAlive(self):
        return self.hp > 0

    # Convert the player data to a JSON data dump
    def toJSON(self):
        jData = {}
        jData['pName'] = self.pName
        jData['pClass'] = self.pClass
        jData['inventory'] = self.inventory
        jData['equipment'] = self.equipment
        jData['level'] = self.level
        jData['hp'] = self.hp
        jData['exp'] = self.exp
        jData['expRate'] = self.expRate
        jData['gold'] = self.gold
        jData['goldRate'] = self.goldRate
        jData['upgradesAvailable'] = self.upgradesAvailable
        jData['stats'] = self.stats
        return jData
