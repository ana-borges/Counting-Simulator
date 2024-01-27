import random
import time

from reaction import WrongNumber


class LevelInterface:
    def start(self):
        pass

    def is_started(self) -> bool:
        pass

    def check_time_left(self) -> int:
        pass

    def register_answer(self, answer: str):
        pass

    def __on_wrong_number(self):
        pass

    def __on_no_number(self):
        pass

    def __on_timeout(self):
        pass

    def __on_correct_answer(self):
        pass


class SheepLevel(LevelInterface):
    def __init__(self, question: str, difficulty: int, initial_timer: int = 60):
        self._startLevelTime: int = -1
        self._stopLevelTime: int = -1
        self.answer: str = ""
        self.question = question
        self._amountOfObjects = random.randint(difficulty * 10, difficulty * 20)
        self._initialTimer = initial_timer

    def start(self):
        self._startLevelTime = int(time.time())
        return

    def is_started(self) -> bool:
        return self._startLevelTime != -1

    def check_time_left(self) -> int:
        if int(time.time()) - self._startLevelTime >= self._initialTimer:
            self.__on_timeout()
        elif self._stopLevelTime != -1:
            return self._initialTimer - (self._stopLevelTime - self._startLevelTime)
        return self._initialTimer - (int(time.time()) - self._startLevelTime)

    def register_answer(self, answer: str):
        self.answer = answer
        if not answer.isdigit():
            return self.__on_no_number()
        elif int(answer) == self._amountOfObjects:
            self.__on_correct_answer()
        return self.__on_wrong_number()

    def __on_wrong_number(self):
        WrongNumber().execute()
        pass

    def __on_no_number(self):
        pass

    def __on_timeout(self):
        pass

    def __on_correct_answer(self):
        pass


level: LevelInterface = SheepLevel("", 1)
