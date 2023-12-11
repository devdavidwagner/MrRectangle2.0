from enum import Enum

class State(Enum):
    MENU = 1
    GAME = 2
    DEATH = 3
    RESTART = 4
    WIN = 5
    GAME_OVER = 6

class GameState:
    __instance = None
    def __init__(self):
        if GameState.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            GameState.__instance = self
            self.scoreUpdated = False
            self.state = State.MENU
            self.score = 0
            self.level = 3
            self.playerLives = 3

    @staticmethod
    def get_instance():
        if GameState.__instance is None:
            GameState.__instance = GameState()
        return GameState.__instance

    def resetLives(self):
        self.playerLives = 3
    
    def resetLevels(self):
        self.level = 1

    def remove_player_life(self):
        self.playerLives -= 1

    def get_player_life(self):
        return self.playerLives
    
    def add_player_life(self):
        self.playerLives +=1
    
    def set_score(self, new_score):
        self.score = new_score

    def set_high_score_updated(self, set):
        self.scoreUpdated = set
    
    def check_high_score_updated(self):
        return self.scoreUpdated

    def get_score(self):
        return self.score

    def next_level(self):
        self.level += 1 

    def return_level(self):
        return self.level