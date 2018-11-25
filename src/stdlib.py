'''
@title Text Adventure: Standard Libraries
@author Carlos Barcelos
@date 23 November 2018

Standard libraries for generic use.
'''

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
