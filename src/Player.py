'''
@title Text Adventure: Player Class
@author Carlos Barcelos
@date TODO

The player class with member veriables and functions.
'''

from random import randint # Pseudo-random numbers

from src.Item import Item           # Work with Item objects
from src.Story import Story         # Work with Story objects
from src.Equipment import Equipment # Work with Equipment objects

MAX_EXP = 100
MIN_STAT_UP = 4
MAX_STAT_UP = 5
MAX_STAT_VAL = 100

eqStructure={"head":"", "chest":"", "legs":"","necklace":"", "ring":"", "staff":""} # Equipment dictionary structure
stStructure={"ATK":0, "INT":0, "DEF":0} # Stats dictionary structure

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

# Set the player stats based on their selected class
def setPlayerStats(pClass):
    # ATK Class
    if pClass == 'Brute':
        stats = {'ATK' : [10, 20], 'INT' : [5, 10], 'DEF' : [0, 5]}
    # INT Class
    elif pClass == 'Scholar':
        stats = {'ATK' : [0, 5], 'INT' : [10, 20], 'DEF' : [5, 10]}
    # DEF Class
    elif pClass == 'Defender':
        stats = {'ATK' : [5, 10], 'INT' : [0, 5], 'DEF' : [10, 20]}
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
        print(f'===== {self.pName} =====')
        print(f'== Class: Level {self.level} {self.pClass}')
        print(f'== HP: {self.hp} / {self.MAX_HP}')
        if self.upgradesAvailable:
            print(f'== Exp ({self.upgradesAvailable}): {self.exp} / {MAX_EXP}')
        else:
            print(f'== Exp: {self.exp} / {MAX_EXP}')
        print(f'== Gold: {self.gold}')
        print(f"== ATK: {self.stats['ATK'][0]}..{self.stats['ATK'][1]}")
        print(f"== INT: {self.stats['INT'][0]}..{self.stats['INT'][1]}")
        print(f"== DEF: {self.stats['DEF'][0]}..{self.stats['DEF'][1]}")
        print(f'=====================')

    # Print the player inventory
    # TODO Handle -l
    def printInventory(self, options):
        print(f'===== Inventory =====')
        for i in self.inventory:
            print(f'== {str(i)}')
        print(f'=====================')

    # Print the player equipment list
    # TODO Handle -l
    def printEquipment(self, options):
        print(f'===== Equipment =====')
        for e in self.equipment.keys():
            print(f'== {e} : {self.equipment[e]}')
        print(f'=====================')

    # Gain additional Exp
    def getExp(self, val):
        val += int(round(self.expRate)) # Apply Exp rate
        prevLevel = self.level
        self.level += (self.exp + val) // MAX_EXP
        self.upgradesAvailable += (self.exp + val) // MAX_EXP
        self.exp = (self.exp + val) % MAX_EXP

        # Handle level up
        if self.level > prevLevel:
            self.hp = self.MAX_HP
            print('Level Up!')

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
        for s in ['ATK', 'INT', 'DEF']:
            if self.stats[s][0] != MAX_STAT_VAL and self.stats[s][1] != MAX_STAT_VAL:
                availableStats.append(s)

        if not availableStats:
            print('There are no stats available to upgrade.')
            return False

        selectedStat = optionParse('Select a stat to upgrade:', availableStats)

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

        selectedAttr = optionParse('Select an attribute to upgrade', availableAttr)

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
            # If this is an item
            if i[:3] == 'it_':
                print('TODO Handle Item')
                returnValue = True

            # If this is a piece of equipment
            elif i[:3] == 'eq_':
                try:
                    lookupEq = resources['equipment'][i]
                    e = Equipment(lookupEq['name'],lookupEq['description'],lookupEq['position'],lookupEq['attribute'],lookupEq['value'])
                    print(f'You got: {str(e)}')
                    self.inventory.append(e)
                    returnValue = True
                except KeyError:
                    print(f'Exception Caught. KeyError: {i}')

            # If this is a story log
            elif i[:3] == 'st_':
                try:
                    lookupSt = resources['story'][i]
                    s = Story(lookupSt['name'],lookupSt['description'],lookupSt['text'])
                    print(f'You got: {str(s)}')
                    self.inventory.append(s)
                    returnValue = True
                except KeyError:
                    print(f'Exception Caught. KeyError: {i}')

            # If this is anything else
            else:
                print(f'{i} is not a supported item type.')
                self.inventory.append(i)
                returnValue = True

        return returnValue

    # Check the player inventory for a certain number of an item
    def checkInventory(self, item, quantity):
        # TODO
        return False

    # Do battle with some enemy
    def battle(self, e, statTuple):
        # Enemy battle information
        statType = statTuple[0]
        eStatVal = statTuple[1]

        # Get the players battle value from within the range
        pStatVal = randint(self.stats[statType][0], self.stats[statType][1])

        print(f'=== {statType} Battle ===')
        print(f'= {self.pName}: {pStatVal}')
        print(f'= Enemy: {eStatVal}')
        print(f'==================')

        return pStatVal > eStatVal

    # Start a 'top trumps' battle with an enemy
    def topTrumpBattle(self, e):
        eStats = list(e['Stats'].keys())

        # Report the stats comparison
        # TODO: Make this look nicer
        print('=== Stat Comparison ===')
        print('=      Player | Enemy =')
        for s in eStats:
            pStatMin = self.stats[s][0]
            pStatMax = self.stats[s][1]
            eStat = e['Stats'][s]
            print(f'= {s}: {pStatMin}..{pStatMax} | {eStat}')
        print(f'======================')

        # Ask player which stat to battle
        selectedStat = optionParse('Select stat to use in battle:', eStats)

        # Get the enemy value and return the battle
        statTuple = (selectedStat, e['Stats'][selectedStat])
        return self.battle(e, statTuple)


    # Equip a piece of equipment
    # TODO Make this work for secondary equipment
    def equip(self, noun, options):
        if noun is None:
            print('Equip requires a noun as input.')
            return False

        equipment = noun + ' ' + ' '.join(options)
        if equipment not in [str(i) for i in self.inventory]:
            print(f'{equipment} is not in your inventory.')
            return False

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
                    print(i.attribute)
                    if i.attribute in ['hp','expRate','goldRate']:
                        print(self.expRate)
                        setattr(self, i.attribute, getattr(self, i.attribute) + i.value)
                        print(self.expRate)
                    # Primary Equipment
                    else:
                        self.stats[i.attribute][0] += i.value
                        self.stats[i.attribute][1] += i.value
        return True

    # Unequip a piece of equipment
    # TODO Make this work for secondary equipment
    def unequip(self, noun, options):
        if noun is None:
            print('Equip requires a noun as input.')
            return False

        equipment = noun + ' ' + ' '.join(options)
        if equipment not in [str(i) for i in self.equipment.values()]:
            print(f'{equipment} is not equiped.')
            return False

        # Move equipment from equipment slot to inventory
        for pos, e in self.equipment.items():

            if str(e) == equipment:
                # Remove status effects
                # Secondary Equipment
                if e.attribute in ['hp','expRate','goldRate']:
                    print(self.expRate)
                    setattr(self, e.attribute, getattr(self, e.attribute) - e.value)
                    print(self.expRate)
                # Primary Equipment
                else:
                    self.stats[e.attribute][0] -= e.value
                    self.stats[e.attribute][1] -= e.value

                # Do the move
                self.equipment[pos] = ''
                self.inventory.append(e)

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
