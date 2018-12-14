'''
@title Text Adventure: Standard Libraries
@author Carlos Barcelos
@date 23 November 2018

Standard libraries for generic use.
'''

from src.Item import Item           # Work with Item objects
from src.Story import Story         # Work with Story objects
from src.Equipment import Equipment # Work with Equipment objects

# Provide a user propt with a given question and acceptible responses
def optionParse(question, answers):
    while "invalid response":
        prettyAnswers = ' ('
        for i in range(len(answers)):
            prettyAnswers += str(answers[i])
            if not i == len(answers)-1:
                prettyAnswers += '/'

        reply = str(input(question+prettyAnswers+')> ')).lower()
        if reply in [a.lower() for a in answers]:
            return reply

# Pretty print a list of text
def prettyPrint(header, body):
    maxWidth = len(header)
    for t in body:
        maxWidth = max(maxWidth, len(t))

    # Print the header
    padding = maxWidth - len(header) + 1
    print(f"+- {header} {padding*'-'}+")\
    # Print the body
    for t in body:
        padding = maxWidth - len(t) + 2
        print(f"| {t}{padding*' '} |")
    # Print the footer
    print(f"+{(maxWidth+4)*'-'}+")

# Get an item object from it's dictionary name
def itemNameToObject(item, resources):
    try:
        # If this is an item
        if item[:3] == 'it_':
            lookupEq = resources['items'][item]
            return Item(lookupEq['name'],lookupEq['description'],lookupEq['usable'],lookupEq['uses'],lookupEq['count'])

        # If this is a piece of equipment
        elif item[:3] == 'eq_':
            lookupEq = resources['equipment'][item]
            return Equipment(lookupEq['name'],lookupEq['description'],lookupEq['position'],lookupEq['attribute'],lookupEq['value'])

        # If this is a story log
        elif item[:3] == 'st_':
            lookupSt = resources['story'][item]
            return Story(lookupSt['name'],lookupSt['description'],lookupSt['text'])

        # If this is anything else
        else:
            print(f'{item} is not a supported item type.')
            return None

    except KeyError:
        print(f'Exception Caught. KeyError: {item}')
        return None

# Get the oppisite of the input direction
def getOppDir(dir):
    if dir == 'north': return 'south'
    elif dir == 'south': return 'north'
    elif dir == 'east': return 'west'
    elif dir == 'west': return 'east'
    else: return None
