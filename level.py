import random
import time

class Level:
    startLevelTime = None

    def __init__(self, question, failureSound, amountOfObject=None, initialTimer=60):
        self.question = question
        self.amountOfObject = amountOfObject
        if amountOfObject is None:
            self.amountOfObject = random.randint(0, 10)
        self.initialTimer = initialTimer
        self.failureSound = "sounds/" + failureSound

    def __str__(self):
        return "question: " + self.question + "\nnumber of objects: " + str(
            self.amountOfObject) + "\ninitial timer(seconds): " + str(self.initialTimer)

    def start(self):
        self.startLevelTime = int(time.time())
        return

    def isLevelFinished(self):
        return int(time.time()) - self.startLevelTime >= self.initialTimer

    def timeLeft(self):
        return self.initialTimer - (int(time.time()) - self.startLevelTime)


levelOne = Level("what is my age", "uh_you_suck.wav", 2, 5)

print(levelOne)

levelOne.start()

while levelOne.isLevelFinished() is not True:
    time.sleep(1)
    print("time remaining: " + str(levelOne.timeLeft()))