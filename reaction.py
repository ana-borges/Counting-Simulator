import random
import pygame as pg
import counting_objects as co


class ReactionInterface:
    def execute(self):
        pass


class WrongNumber(ReactionInterface):
    def __init__(self):
        self._soundFile: str = random.choice(["sounds/UH_YOU_SUCK.wav"])
        self._failureSound = pg.mixer.Sound(self._soundFile)
        return

    def execute(self):
        pg.mixer.Sound.play(self._failureSound)
        return


class NoNumber(ReactionInterface):
    def __init__(self):
        self._soundFile: str = random.choice(["sounds/ARE_YOU_DUMB_THIS_IS_NOT_EVEN_A_NUMBER.wav"])
        self._failureSound = pg.mixer.Sound(self._soundFile)
        return

    def execute(self):
        pg.mixer.Sound.play(self._failureSound)
        return

class Timout(ReactionInterface):
    def __init__(self):
        self._soundFile: str = random.choice(["sounds/YOUR_MUM_IS_SO_SLOW.wav"])
        self._failureSound = pg.mixer.Sound(self._soundFile)
        return

    def execute(self):
        pg.mixer.Sound.play(self._failureSound)
        return

class Correct(ReactionInterface):
    def __init__(self, all_objects: pg.sprite.Group):
        self._soundFile: str = random.choice(["sounds/YOUR_MUM_IS_SO_SLOW.wav"])
        self._failureSound = pg.mixer.Sound(self._soundFile)
        self._allObjects = all_objects
        return

    def execute(self) -> pg.sprite.Group:
        new_sheep = co.generateHerd(1)
        self._allObjects.add(new_sheep)
        pg.mixer.Sound.play(self._failureSound)
        return self._allObjects
