import random
import pygame as pg
import counting_objects as co

ask_picture_question: bool = False
deadSheep: bool = False
win: bool = False


class ReactionInterface:
    def execute(self):
        pass


class WrongNumber(ReactionInterface):
    def execute(self):
        sound_file: str = random.choice(["sounds/UH_YOU_SUCK.wav", "sounds/BUZZER.wav"])
        pg.mixer.Sound.play(pg.mixer.Sound(sound_file))
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
        self._soundFile: str = random.choice(["sounds/SO_CLOSE.wav"])
        self._failureSound = pg.mixer.Sound(self._soundFile)
        self._allObjects = all_objects
        return

    def execute(self) -> pg.sprite.Group:
        new_sheep = co.generateHerd(1)
        self._allObjects.add(new_sheep)
        pg.mixer.Sound.play(self._failureSound)
        return self._allObjects


class CorrectPicture(ReactionInterface):
    def __init__(self, all_objects: pg.sprite.Group):
        self._soundFile: str = random.choice(["sounds/PICTURE_QUESTION.wav"])
        self._failureSound = pg.mixer.Sound(self._soundFile)
        self._allObjects = all_objects
        return

    def execute(self) -> pg.sprite.Group:
        pg.mixer.Sound.play(self._failureSound)
        global ask_picture_question
        ask_picture_question = True
        return self._allObjects


class DeadSheep(ReactionInterface):
    def __init__(self, all_objects: pg.sprite.Group):
        self._soundFile: str = random.choice(["sounds/DEAD_SHEEP.wav"])
        self._failureSound = pg.mixer.Sound(self._soundFile)
        self._allObjects = all_objects
        return

    def execute(self):
        global deadSheep
        deadSheep = True
        pg.mixer.Sound.play(self._failureSound)
        return self._allObjects


class Winning(ReactionInterface):
    def execute(self):
        global win
        win = True
        pg.mixer.Sound.play(pg.mixer.Sound("sounds/WIN.wav"))
        return


class LevelProgression(ReactionInterface):
    def __init__(self, version: int):
        self._failureSound = pg.mixer.Sound("sounds/LEVEL_PROGRESSION_" + str(version) + ".wav")
        return

    def execute(self):
        pg.mixer.Sound.play(self._failureSound)
        return
