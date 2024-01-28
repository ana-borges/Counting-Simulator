import random
import time
import pygame as pg

from reaction import WrongNumber, NoNumber, Timeout, Correct, CorrectPicture, DeadSheep, Winning, LevelProgression


class LevelInterface:
    def start(self):
        pass

    def is_started(self) -> bool:
        pass

    def check_time_left(self) -> int:
        pass

    def register_answer(self, answer: str, all_objects: pg.sprite.Group) -> pg.sprite.Group:
        pass

    def __on_wrong_number(self):
        pass

    def __on_no_number(self):
        pass

    def __on_timeout(self):
        pass

    def __on_correct_answer(self, all_objects: pg.sprite.Group):
        pass

    def get_amount_of_objects(self) -> int:
        pass

    def is_stopped(self) -> bool:
        pass

    def get_question(self) -> str:
        pass

    def reset(self):
        pass

    def __on_winning(self):
        pass

    def __check_for_level_progression(self) -> bool:
        pass

    def __on_level_progression(self):
        pass


class GoatLevel(LevelInterface):
    def __init__(self, question: str, difficulty: int):
        self._startLevelTime: int = -1
        self._stopLevelTime: int = -1
        self.answer: str = ""
        self.question = question
        self.difficulty = difficulty
        self._amountOfObjects = random.randint(difficulty * 10 + 5, difficulty * 20 + 10)
        self._initialTimer = 10
        self.number_correct = 0
        self.number_incorrect = 0

    def start(self):
        self._startLevelTime = int(time.time())
        return

    def is_started(self) -> bool:
        return self._startLevelTime != -1

    def check_time_left(self) -> int:
        if self._stopLevelTime != -1:
            return self._initialTimer - (self._stopLevelTime - self._startLevelTime)
        elif int(time.time()) - self._startLevelTime >= self._initialTimer:
            self._stopLevelTime = int(time.time())
            self.__on_timeout()
            return 0
        return self._initialTimer - (int(time.time()) - self._startLevelTime)

    def register_answer(self, answer: str, all_objects: pg.sprite.Group):
        self._stopLevelTime = int(time.time())
        self.answer = answer
        if not answer.isdigit():
            self.__on_no_number()
            return all_objects
        elif f'{int(self._amountOfObjects):0b}' == answer:
            self.__on_winning()
            return all_objects
        elif int(answer) == self._amountOfObjects:
            return self.__on_correct_answer(all_objects)
        else:
            self.__on_wrong_number()
            return all_objects

    def __on_wrong_number(self):
        self.number_incorrect += 1
        if self.__check_for_level_progression():
            self.__on_level_progression()
        else:
            WrongNumber().execute()
        return

    def __on_no_number(self):
        self.number_incorrect += 1
        if self.__check_for_level_progression():
            self.__on_level_progression()
        else:
            NoNumber().execute()
        return

    def __on_timeout(self):
        self.number_incorrect += 1
        if self.__check_for_level_progression():
            self.__on_level_progression()
        else:
            Timeout().execute()
        return

    def __on_correct_answer(self, all_objects: pg.sprite.Group) -> pg.sprite.Group:
        self.number_correct += 1
        return random.choice([Correct(all_objects), CorrectPicture(all_objects), DeadSheep(all_objects)]).execute()

    def get_amount_of_objects(self) -> int:
        return self._amountOfObjects

    def is_stopped(self) -> bool:
        return self._stopLevelTime != -1

    def get_question(self) -> str:
        return self.question

    def get_number_correct(self) -> int:
        return self.number_correct

    def reset(self):
        self._startLevelTime: int = -1
        self._stopLevelTime: int = -1
        self.answer: str = ""
        self._amountOfObjects = random.randint(self.difficulty * 10 + 5, self.difficulty * 20 + 10)
        self.start()

    def __on_winning(self):
        Winning().execute()
        return

    def __check_for_level_progression(self) -> bool:
        return self.number_incorrect != 0 and self.number_incorrect % 5 == 0

    def __on_level_progression(self):
        next_level = int(self.number_incorrect/5) % 3
        if next_level == 1:
            self.difficulty = 0
        elif next_level == 2:
            self.difficulty = 10
        elif next_level == 0:
            self.difficulty = 1
        LevelProgression(next_level).execute()
        return
