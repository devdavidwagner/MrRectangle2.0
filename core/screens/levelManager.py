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
        self.enemyYRow = 96
    
        spriteSheet = SpriteSheet("assets\sprites\spriteSheet.png")
       # 0, 14, 28, 42, 56, 70,
      
        imageCharStillRight = spriteSheet.load_image(0,0,self.spriteWidth, self.spriteHeight) 
        imageCharMoveRight = spriteSheet.load_image(self.spriteWidth,0,self.spriteWidth, self.spriteHeight)
        imageCharMoveRight2 = spriteSheet.load_image(self.spriteWidth * 2,0,self.spriteWidth, self.spriteHeight)
        imageCharMoveRight3 = spriteSheet.load_image(self.spriteWidth * 3,0,self.spriteWidth, self.spriteHeight)     
        imageJumpingRight = spriteSheet.load_image(self.spriteWidth * 4 ,0,self.spriteWidth, self.spriteHeight)
        imageJumpingRight2 = spriteSheet.load_image(self.spriteWidth * 5 ,0,self.spriteWidth, self.spriteHeight)
        imageJumpingRight3 = spriteSheet.load_image(self.spriteWidth * 6 ,0,self.spriteWidth, self.spriteHeight)
        imageCharStillLeft = spriteSheet.load_image(self.spriteWidth * 7,0,self.spriteWidth, self.spriteHeight)
        imagecharMoveLeft = spriteSheet.load_image(self.spriteWidth * 8,0,self.spriteWidth, self.spriteHeight)
        imagecharMoveLeft2 = spriteSheet.load_image(self.spriteWidth * 9,0,self.spriteWidth, self.spriteHeight)
        imagecharMoveLeft3 = spriteSheet.load_image(self.spriteWidth * 10,0,self.spriteWidth, self.spriteHeight)
        imageJumpingLeft = spriteSheet.load_image(self.spriteWidth * 11,0,self.spriteWidth, self.spriteHeight)
        imageJumpingLeft2 = spriteSheet.load_image(self.spriteWidth * 12,0,self.spriteWidth, self.spriteHeight)
        imageJumpingLeft3 = spriteSheet.load_image(self.spriteWidth * 13,0,self.spriteWidth, self.spriteHeight)
        imageShootingRight = spriteSheet.load_image(self.spriteWidth * 14,0,self.spriteWidth, self.spriteHeight)     
        imageShootingRight2 = spriteSheet.load_image(self.spriteWidth * 15,0,self.spriteWidth, self.spriteHeight)     
        imageShootingRight3 = spriteSheet.load_image(self.spriteWidth * 16,0,self.spriteWidth, self.spriteHeight)     
        imageShootingRight4 = spriteSheet.load_image(self.spriteWidth * 17,0,self.spriteWidth, self.spriteHeight)  
        deadRight = spriteSheet.load_image(self.spriteWidth * 18,0,self.spriteWidth, self.spriteHeight)  
        deadRight2 = spriteSheet.load_image(self.spriteWidth * 19,0,self.spriteWidth, self.spriteHeight) 
        deadRight3 = spriteSheet.load_image(self.spriteWidth * 20,0,self.spriteWidth, self.spriteHeight) 
        deadRight4 = spriteSheet.load_image(self.spriteWidth * 21,0,self.spriteWidth, self.spriteHeight) 
        ducking = spriteSheet.load_image(self.spriteWidth * 22,0,self.spriteWidth, self.spriteHeight) 
        ducking2 = spriteSheet.load_image(self.spriteWidth * 23,0,self.spriteWidth, self.spriteHeight) 
        ducking3 = spriteSheet.load_image(self.spriteWidth * 24,0,self.spriteWidth, self.spriteHeight) 
        falling1 = spriteSheet.load_image(self.spriteWidth * 25,0,self.spriteWidth, self.spriteHeight) 
        falling2 = spriteSheet.load_image(self.spriteWidth * 26,0,self.spriteWidth, self.spriteHeight) 

        imageCharStillRightUpgrade1 = spriteSheet.load_image(0,self.spriteHeight,self.spriteWidth, self.spriteHeight) 
        imageCharMoveRightUpgrade1 = spriteSheet.load_image(self.spriteWidth,self.spriteHeight,self.spriteWidth, self.spriteHeight)
        imageCharMoveRight2Upgrade1 = spriteSheet.load_image(self.spriteWidth * 2,self.spriteHeight,self.spriteWidth, self.spriteHeight)
        imageCharMoveRight3Upgrade1 = spriteSheet.load_image(self.spriteWidth * 3,self.spriteHeight,self.spriteWidth, self.spriteHeight)     
        imageJumpingRightUpgrade1 = spriteSheet.load_image(self.spriteWidth * 4 ,self.spriteHeight,self.spriteWidth, self.spriteHeight)
        imageJumpingRight2Upgrade1 = spriteSheet.load_image(self.spriteWidth * 5 ,self.spriteHeight,self.spriteWidth, self.spriteHeight)
        imageJumpingRight3Upgrade1 = spriteSheet.load_image(self.spriteWidth * 6 ,self.spriteHeight,self.spriteWidth, self.spriteHeight)
        imageCharStillLeftUpgrade1 = spriteSheet.load_image(self.spriteWidth * 7,self.spriteHeight,self.spriteWidth, self.spriteHeight)
        imagecharMoveLeftUpgrade1 = spriteSheet.load_image(self.spriteWidth * 8,self.spriteHeight,self.spriteWidth, self.spriteHeight)
        imagecharMoveLeft2Upgrade1 = spriteSheet.load_image(self.spriteWidth * 9,self.spriteHeight,self.spriteWidth, self.spriteHeight)
        imagecharMoveLeft3Upgrade1 = spriteSheet.load_image(self.spriteWidth * 10,self.spriteHeight,self.spriteWidth, self.spriteHeight)
        imageJumpingLeftUpgrade1 = spriteSheet.load_image(self.spriteWidth * 11,self.spriteHeight,self.spriteWidth, self.spriteHeight)
        imageJumpingLeft2Upgrade1 = spriteSheet.load_image(self.spriteWidth * 12,self.spriteHeight,self.spriteWidth, self.spriteHeight)
        imageJumpingLeft3Upgrade1 = spriteSheet.load_image(self.spriteWidth * 13,self.spriteHeight,self.spriteWidth, self.spriteHeight)
        imageShootingRightUpgrade1 = spriteSheet.load_image(self.spriteWidth * 14,self.spriteHeight,self.spriteWidth, self.spriteHeight)     
        imageShootingRight2Upgrade1 = spriteSheet.load_image(self.spriteWidth * 15,self.spriteHeight,self.spriteWidth, self.spriteHeight)     
        imageShootingRight3Upgrade1 = spriteSheet.load_image(self.spriteWidth * 16,self.spriteHeight,self.spriteWidth, self.spriteHeight)     
        imageShootingRight4Upgrade1 = spriteSheet.load_image(self.spriteWidth * 17,self.spriteHeight,self.spriteWidth, self.spriteHeight)  
        deadRightUpgrade1 = spriteSheet.load_image(self.spriteWidth * 18,self.spriteHeight,self.spriteWidth, self.spriteHeight)  
        deadRight2Upgrade1 = spriteSheet.load_image(self.spriteWidth * 19,self.spriteHeight,self.spriteWidth, self.spriteHeight) 
        deadRight3Upgrade1 = spriteSheet.load_image(self.spriteWidth * 20,self.spriteHeight,self.spriteWidth, self.spriteHeight) 
        deadRight4Upgrade1 = spriteSheet.load_image(self.spriteWidth * 21,self.spriteHeight,self.spriteWidth, self.spriteHeight) 
        duckingUpgrade1 = spriteSheet.load_image(self.spriteWidth * 22,self.spriteHeight,self.spriteWidth, self.spriteHeight) 
        ducking2Upgrade1 = spriteSheet.load_image(self.spriteWidth * 23,self.spriteHeight,self.spriteWidth, self.spriteHeight) 
        ducking3Upgrade1 = spriteSheet.load_image(self.spriteWidth * 24,self.spriteHeight,self.spriteWidth, self.spriteHeight) 
        falling1Upgrade1 = spriteSheet.load_image(self.spriteWidth * 25,self.spriteHeight,self.spriteWidth, self.spriteHeight) 
        falling2Upgrade1 = spriteSheet.load_image(self.spriteWidth * 26,self.spriteHeight,self.spriteWidth, self.spriteHeight) 

        playerProjectile = pygame.image.load("assets\sprites\PlayerShot.png").convert_alpha()

        enemyLeft = spriteSheet.load_image(0,self.enemyYRow ,self.enemyWidth, self.enemyHeight)     
        enemyLeft2 = spriteSheet.load_image(self.enemyWidth,self.enemyYRow ,self.enemyWidth, self.enemyHeight)     
        enemyLeft3 = spriteSheet.load_image(self.enemyWidth * 2,self.enemyYRow ,self.enemyWidth, self.enemyHeight) 
        enemyDead1 = spriteSheet.load_image(self.enemyWidth * 3,self.enemyYRow,self.enemyWidth, self.enemyHeight)  
        enemyDead2 = spriteSheet.load_image(self.enemyWidth * 4,self.enemyYRow,self.enemyWidth, self.enemyHeight)  
        enemyDead3 = spriteSheet.load_image(self.enemyWidth * 5,self.enemyYRow,self.enemyWidth, self.enemyHeight)  

        enemyLeft = pygame.transform.scale(enemyLeft, (100, 70))
        enemyLeft2 = pygame.transform.scale(enemyLeft2, (100, 70))
        enemyLeft3 = pygame.transform.scale(enemyLeft3, (100, 70))
        enemyDead1 = pygame.transform.scale(enemyDead1, (100, 70))
        enemyDead2 = pygame.transform.scale(enemyDead2, (100, 70))
        enemyDead3 = pygame.transform.scale(enemyDead3, (100, 70))

        
        platformSmall = pygame.image.load("assets\sprites\SmallPlatform.png").convert_alpha()
        platformStart = pygame.image.load("assets\sprites\StartPlatform.png").convert_alpha()
        platformBig = pygame.image.load("assets\sprites\BigPlatform.png").convert_alpha()
        platformEnd = pygame.image.load("assets\sprites\EndPlatform.png").convert_alpha()
        
        para0 = pygame.image.load("assets\sprites\para0.png").convert_alpha()
        para1 = pygame.image.load("assets\sprites\para1.png").convert_alpha()
        para2 = pygame.image.load("assets\sprites\para2.png").convert_alpha()
        para3 = pygame.image.load("assets\sprites\para3.png").convert_alpha()

        splat = pygame.image.load("assets\sprites\splat.png").convert_alpha()
        splat2 = pygame.image.load("assets\sprites\splat2.png").convert_alpha()
        splat3 = pygame.image.load("assets\sprites\splat3.png").convert_alpha()

        fruit = pygame.image.load("assets\sprites\\fruit.png").convert_alpha()
        fruit2 = pygame.image.load("assets\sprites\\fruit2.png").convert_alpha()
        fruit3 = pygame.image.load("assets\sprites\\fruit3.png").convert_alpha()
        fruit4 = pygame.image.load("assets\sprites\\fruit4.png").convert_alpha()
        self.fruitImages = [fruit, fruit2, fruit3, fruit4]

        jumpBlock = pygame.image.load("assets\sprites\\jumpBlock.png").convert_alpha()
        jumpBlock2 = pygame.image.load("assets\sprites\\jumpBlock2.png").convert_alpha()
        self.jumpBlockImages = [jumpBlock, jumpBlock2]

        diamond = pygame.image.load("assets\sprites\\diamond.png").convert_alpha()
        diamond2 = pygame.image.load("assets\sprites\\diamond2.png").convert_alpha()
        diamond3 = pygame.image.load("assets\sprites\\diamond3.png").convert_alpha()
        diamond4 = pygame.image.load("assets\sprites\\diamond4.png").convert_alpha()
        self.diamondImages = [diamond,diamond2,diamond3,diamond4]

        life = pygame.image.load("assets\sprites\\life.png").convert_alpha()
        life2 = pygame.image.load("assets\sprites\\life2.png").convert_alpha()
        life3 = pygame.image.load("assets\sprites\\life3.png").convert_alpha()
        life4 = pygame.image.load("assets\sprites\\life4.png").convert_alpha()
        self.lifeImages = [life,life2,life3,life4]

        playerProjectileUpgraded = pygame.image.load("assets\sprites\\PlayerShotUpgraded.png").convert_alpha()
        upgradeEffect = pygame.image.load("assets\sprites\\upgradeEffect.png").convert_alpha()
        upgradeEffect2 = pygame.image.load("assets\sprites\\upgradeEffect2.png").convert_alpha()
        upgradeEffect3 =  pygame.image.load("assets\sprites\\upgradeEffect3.png").convert_alpha()

        spikeImage =  pygame.image.load("assets\sprites\\spikes.png").convert_alpha()
        self.spikeImage = spikeImage

        self.playerImages = [imageCharStillLeft, imageCharStillRight, imagecharMoveLeft,imagecharMoveLeft2,imagecharMoveLeft3,imageCharMoveRight, imageCharMoveRight2 ,imageCharMoveRight3 ,imageJumpingLeft,imageJumpingLeft2,imageJumpingLeft3, imageJumpingRight, imageJumpingRight2, imageJumpingRight3, imageShootingRight, imageShootingRight2, imageShootingRight3,imageShootingRight4, playerProjectile, deadRight, deadRight2, deadRight3, deadRight4, ducking, ducking2,ducking3, falling1,falling2, playerProjectileUpgraded, upgradeEffect, upgradeEffect2, upgradeEffect3]
        self.playerImagesUpgrade1 = [imageCharStillLeftUpgrade1, imageCharStillRightUpgrade1, imagecharMoveLeftUpgrade1,imagecharMoveLeft2Upgrade1,imagecharMoveLeft3Upgrade1,imageCharMoveRightUpgrade1, imageCharMoveRight2Upgrade1 ,imageCharMoveRight3Upgrade1 ,imageJumpingLeftUpgrade1,imageJumpingLeft2Upgrade1,imageJumpingLeft3Upgrade1, imageJumpingRightUpgrade1, imageJumpingRight2Upgrade1, imageJumpingRight3Upgrade1, imageShootingRightUpgrade1, imageShootingRight2Upgrade1, imageShootingRight3Upgrade1,imageShootingRight4Upgrade1, playerProjectile, deadRightUpgrade1, deadRight2Upgrade1, deadRight3Upgrade1, deadRight4Upgrade1, duckingUpgrade1, ducking2Upgrade1,ducking3Upgrade1, falling1Upgrade1,falling2Upgrade1, playerProjectileUpgraded, upgradeEffect, upgradeEffect2, upgradeEffect3]
        self.platformImages = [platformStart, platformSmall, platformBig, platformEnd]
        self.parallaxImages = [para0, para1, para2, para3] #BACKGROUNDS
        self.effectImages = [splat,splat2,splat3]
        self.soundEffects = ["assets\sounds\LaserShot.wav", "assets\sounds\JetPack.wav","assets\sounds\Hit.wav", "assets\sounds\EnemyHit.wav"]
        self.enemyImages = [enemyLeft, enemyLeft2, enemyLeft3, enemyDead1, enemyDead2, enemyDead3]
        self.game_state = GameState.get_instance()
        self.currentLevel = self.game_state.return_level()
     
        self.engine = Engine(self.screen, self.currentLevel, self.screen_width, self.screen_height, self.playerImages,  self.platformImages, self.parallaxImages, self.enemyImages,  self.fruitImages, self.effectImages, self.soundEffects, self.jumpBlockImages, self.diamondImages, self.playerImagesUpgrade1, self.lifeImages, self.spikeImage)


    def runLevel(self):
        self.engine.runGame()
    
    def reset(self):
        self.engine.reset()
        