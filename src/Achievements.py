'''
@title Text Adventure: Achievements Class
@author Carlos Barcelos
@date 20 November 2018

The achievements class with member veriables and functions.
'''

import src.stdlib as std # Import standard libraries

# Upon initialization, check if any achievments are completed
def initCheck(achievements):
    remainingList = []
    for k,v in achievements.items():
        prog = v['Progress']
        progFractionalCompleted = int(prog[0]/prog [1])
        if (progFractionalCompleted != 1):
            remainingList.append(k)
    return remainingList

class Achievements():
    def __init__(self, achFile):
        self.achievements = achFile
        self.remaining = initCheck(achFile)

    # Check if any achievement status has changed
    def checkAll(self, ge):
        # Only check the remaining achievements
        for a in self.remaining:
            ach = self.achievements[a]
            # TODO Check the requirement
            # TODO Update the progress
            # If an achievement has completed, remove it from the remaining list
            if (ach['Progress'][0] // ach['Progress'][1]) == 1:
                self.remaining.remove(a)
        return False

    # Get the progress of a certain achievement
    def getProgress(self, achievement, options):
        bars = 10
        prog = achievement['Progress']
        progFractionalCompleted = int((prog[0]/prog [1])*bars)

        progress = ('#'*progFractionalCompleted) + ('-'*(bars-progFractionalCompleted))
        progressBar = f'[{progress}]'

        if options == '-l':
            progressStr = f"{progressBar} {achievement['Name']} : {achievement['Description']}"
        else:
            progressStr = f"{progressBar} {achievement['Name']}"

        return progressStr

    # Report the progress of in progress Achievements
    # -l : Display ALL achievements with progress
    def reportAll(self, options):
        if options == '-l':
            achievementList = self.achievements
        else:
            achievementList = self.remaining

        # Get the printable text
        body = []
        for a in achievementList:
            progress = self.getProgress(self.achievements[a], options)
            body.append(progress)

        # Hand off the print to the helper
        std.prettyPrint('Achievements', body)
        return True
