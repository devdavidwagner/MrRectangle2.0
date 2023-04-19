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

    @staticmethod
    def get_instance():
        if GameState.__instance == None:
            GameState()
        return GameState.__instance

