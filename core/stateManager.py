from enum import Enum

class State(Enum):
    MENU = 1
    GAME = 2
    DEATH = 3
    RESTART = 4
    WIN = 5

class GameState:
    __instance = None
    def __init__(self):
        if GameState.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            GameState.__instance = self
            self.state = State.MENU
            self.score = 0
            self.level = 1

    @staticmethod
    def get_instance():
        if GameState.__instance is None:
            GameState.__instance = GameState()
        return GameState.__instance


    def set_score(self, new_score):
        self.score = new_score

    def get_score(self):
        return self.score

    def next_level(self):
        self.level += 1 

    def return_level(self):
        return self.level