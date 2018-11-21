'''
@title Text Adventure: Achievements Class
@author Carlos Barcelos
@date TODO

The achievements class with member veriables and functions.
'''

class Achievements():
    def __init__(self, achievement):
        self.achievements = achievement
        self.remaining = list(achievement.keys())

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
    # TODO Where should the description of the achievement go?
    def getProgress(self, achievement):
        bars = 10
        prog = achievement['Progress']
        progFractionalCompleted = int((prog[0]/prog [1])*bars)

        progress = ('#'*progFractionalCompleted) + ('-'*(bars-progFractionalCompleted))
        progressBar = f'[{progress}]'
        return f"{progressBar} {achievement['Name']} : {achievement['Description']}"

    # Report the progress of all achievements
    def reportAll(self):
        for a in self.achievements:
            progress = self.getProgress(self.achievements[a])
            print(progress)
        return True
