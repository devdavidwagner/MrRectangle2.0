from enum import Enum
from core.engine import Engine
from core.stateManager import State, GameState
from core.helpers.spriteSheet import SpriteSheet
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
        self.spriteWidth = 14
        self.spriteHeight = 24

        self.enemyWidth = 25
        self.enemyHeight = 18
        self.enemyYRow = 52
    
        spriteSheet = SpriteSheet("assets\sprites\spriteSheet.png")
       # 0, 14, 28, 42, 56, 70,

        
        imageCharStillRight = spriteSheet.load_image(0,0,self.spriteWidth, self.spriteHeight)  
        imageCharMoveRight = spriteSheet.load_image(self.spriteWidth,0,self.spriteWidth, self.spriteHeight)
        imageJumpingRight = spriteSheet.load_image(self.spriteWidth * 2 ,0,self.spriteWidth, self.spriteHeight)
        
        
        imageCharStillLeft = spriteSheet.load_image(self.spriteWidth * 3,0,self.spriteWidth, self.spriteHeight)       
        imagecharMoveLeft = spriteSheet.load_image(self.spriteWidth * 4,0,self.spriteWidth, self.spriteHeight)
        imageJumpingLeft = spriteSheet.load_image(self.spriteWidth * 5,0,self.spriteWidth, self.spriteHeight)

        enemyLeft = spriteSheet.load_image(0,self.enemyYRow ,self.enemyWidth, self.enemyHeight)     
        enemyLeft2 = spriteSheet.load_image(self.enemyWidth,self.enemyYRow ,self.enemyWidth, self.enemyHeight)     
        enemyLeft3 = spriteSheet.load_image(self.enemyWidth * 2,self.enemyYRow ,self.enemyWidth, self.enemyHeight)  
        
        enemyLeft = pygame.transform.scale(enemyLeft, (100, 70))
        enemyLeft2 = pygame.transform.scale(enemyLeft2, (100, 70))
        enemyLeft3 = pygame.transform.scale(enemyLeft3, (100, 70))

        
        platformSmall = pygame.image.load("assets\sprites\SmallPlatform.png").convert_alpha()
        platformStart = pygame.image.load("assets\sprites\StartPlatform.png").convert_alpha()
        platformBig = pygame.image.load("assets\sprites\BigPlatform.png").convert_alpha()
        platformEnd = pygame.image.load("assets\sprites\EndPlatform.png").convert_alpha()
        
        para0 = pygame.image.load("assets\sprites\para0.png").convert_alpha()
        para1 = pygame.image.load("assets\sprites\para1.png").convert_alpha()
        para2 = pygame.image.load("assets\sprites\para2.png").convert_alpha()
        para3 = pygame.image.load("assets\sprites\para3.png").convert_alpha()
        

        self.playerImages = [imageCharStillLeft, imageCharStillRight, imagecharMoveLeft, imageCharMoveRight ,imageJumpingLeft, imageJumpingRight]
        self.platformImages = [platformStart, platformSmall, platformBig, platformEnd]
        self.parallaxImages = [para0, para1, para2, para3] #BACKGROUNDS
        self.enemyImages = [enemyLeft, enemyLeft2, enemyLeft3]
        self.engine = Engine(self.screen, self.currentLevel, self.screen_width, self.screen_height, self.playerImages,  self.platformImages, self.parallaxImages, self.enemyImages)


    def runLevel(self):
        self.engine.runGame()
    
    def reset(self):
        self.engine.reset()
        
