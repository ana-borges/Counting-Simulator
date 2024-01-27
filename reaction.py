import random
import pygame as pg


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
