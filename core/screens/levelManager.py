from enum import Enum
from core.engine import Engine
from core.stateManager import State, GameState
import pygame

class Level(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4

inGame = True
class LevelManager():
    def __init__(self, currentLevel, screen, screen_width, screen_height):
        self.currentLevel = currentLevel
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.death = False
    

        imageCharStillLeft = pygame.image.load("assets\sprites\RectangleStillLeft.png").convert_alpha()
        imageCharStillRight = pygame.image.load("assets\sprites\RectangleStillRight.png").convert_alpha()      
        imagecharMoveLeft = pygame.image.load("assets\sprites\RectangleMoveLeft.png").convert_alpha()
        imageCharMoveRight = pygame.image.load("assets\sprites\RectangleMoveRight.png").convert_alpha()
        imageJumpingLeft = pygame.image.load("assets\sprites\RectangleJumpingLeft.png").convert_alpha()
        imageJumpingRight = pygame.image.load("assets\sprites\RectangleJumpingRight.png").convert_alpha()

        platformBig = pygame.image.load("assets\sprites\BigPlatform.png").convert_alpha()
        platformSmall = pygame.image.load("assets\sprites\SmallPlatform.png").convert_alpha()
        

        self.playerImages = [imageCharStillLeft, imageCharStillRight, imagecharMoveLeft, imageCharMoveRight ,imageJumpingLeft, imageJumpingRight]
        self.platformImages = [platformBig, platformSmall]
        self.engine = Engine(self.screen, self.currentLevel, self.screen_width, self.screen_height, self.playerImages,  self.platformImages)


    def runLevel(self):
        self.engine.runGame()
    
    def reset(self):
        self.engine.reset()
        
