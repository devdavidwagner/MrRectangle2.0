import pygame
import time
from assets.sprites.objects.rectangle import Rectangle, Direction
from assets.sprites.objects.platform import Platform
from core.stateManager import State, GameState
from core.helpers.collideHelper import CollisionDetection
from core.helpers.backgroundManager import BackgroundManager

class Engine():
    def __init__(self, screen, currentLevel, screen_width, screen_height , playerImages:list, platformImages:list, parallaxImages:list):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.currentLevel = currentLevel
        self.font = pygame.font.Font(None, 36)
        self.bg_color = (255, 255, 255)
        self.startingX = (screen_width / 2) - 50
        self.startingY = 350
        self.startingXPlayer = (screen_width / 2) - 50
        self.startingYPlayer = self.startingY - 64
        self.playerImages = playerImages
        self.platformImages = platformImages
        self.player = Rectangle(self.startingXPlayer, self.startingYPlayer, self.playerImages[1])

        self.platform = Platform(self.startingX, self.startingY, self.platformImages[0])
        self.platformSmall = Platform(self.startingX + 300, self.startingY, self.platformImages[1])

        self.platforms = [self.platform, self.platformSmall]

        self.noMovement = False

        self.parallaxImages = parallaxImages
        self.backgroundManager = BackgroundManager(self.player, self.screen, screen_width, parallaxImages)
        
        

        self.playerImageLeftStill = self.playerImages[0]
        self.playerImageRightStill = self.playerImages[1]
        self.playerImageLeftMoving = self.playerImages[2] 
        self.playerImageRightMoving = self.playerImages[3]
        self.playerImageLeftJumping = self.playerImages[4] 
        self.playerImageRightJumping = self.playerImages[5]
        self.lastDirection = Direction.RIGHT
        self.dt = 0
        
        self.playerOnPlatform = False
        self.noMovement = False

        self.collisionDetect = CollisionDetection()
        
        

    def reset(self):
        self.player = Rectangle(self.startingXPlayer, self.startingYPlayer, self.playerImages[1])

        self.platform = Platform(0, self.startingY + self.player.rect.height, self.platformImages[0])
        self.platformSmall = Platform(self.screen_width + 300, self.startingY + self.player.rect.height, self.platformImages[1])
        self.platformSmall2 = Platform(self.screen_width + self.platformSmall.rect.width + 900, self.startingY + self.player.rect.height, self.platformImages[1])
        self.platformSmall3 = Platform(self.screen_width + 2500, self.startingY + self.player.rect.height, self.platformImages[1])
        self.platforms = [self.platform, self.platformSmall, self.platformSmall2, self.platformSmall3]




    
    def runGame(self):
        ticks = 0
        engineOn = True
        self.objects = pygame.sprite.Group()
        
        customDetect = CollisionDetection()

        #platforms
        platform_group = pygame.sprite.Group()
        for platform in self.platforms:
            platform_group.add(platform)
            self.objects.add(platform)

        #player
        self.objects.add(self.player)

        while engineOn:
            ticks += 1
            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE and not self.player.jumping and not self.player.falling:
                     #JUMPING
                    self.player.jumping = True
           
    
            self.playerOnPlatform = False       

            #collision (on platform)        
            for platform in self.platforms:            
                if self.collisionDetect.check_collisionTop(self.player.rect, platform.rect):
                    self.playerOnPlatform = True
                    break
            
            self.noMovement = False
            #collision (left/right)
            for platform in self.platforms:            
                if self.collisionDetect.check_collisionRight(self.player.rect, platform.rect):
                    self.noMovement = True
                    break
                if self.collisionDetect.check_collisionLeft(self.player.rect, platform.rect):
                    self.noMovement = True
                    break
 
            if self.playerOnPlatform:
                self.player.Action(False, None, False, False)  #on platform
            else:
                self.player.Action(False,  None, True, False) #falling

            keys = pygame.key.get_pressed()

        #KEYS/ACTIONS     
            #JUMPING 
            
            if self.player.jumping == True and self.lastDirection == Direction.RIGHT:
                    self.player.Action(True, Direction.RIGHT,  False, True)
                
            elif self.player.jumping == True and self.lastDirection == Direction.LEFT:
                    self.player.Action(True, Direction.LEFT, False, True)

            #MOVING RIGHT
            stuck = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.Action(True, Direction.RIGHT)
                self.lastDirection = Direction.RIGHT
                self.backgroundManager.update(Direction.RIGHT, self.noMovement)                        
                platform_group.update(self.playerOnPlatform, self.player.rect, Direction.RIGHT, self.noMovement)                
            #MOVING LEFT
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.Action(True, Direction.LEFT)
                self.lastDirection = Direction.LEFT
                self.backgroundManager.update(Direction.LEFT, self.noMovement)                        
                platform_group.update(self.playerOnPlatform, self.player.rect, Direction.LEFT, self.noMovement)                               
            #STILL
            else:
                if self.lastDirection == Direction.RIGHT:
                    self.player.Action(False, Direction.RIGHT)
                elif self.lastDirection == Direction.LEFT:
                    self.player.Action(False, Direction.LEFT)



        #set sprites
            #jumping
            if self.player.jumping and self.lastDirection == Direction.RIGHT:
                self.player.ActiveSprite(self.playerImageRightJumping)
            elif self.player.jumping and self.lastDirection == Direction.LEFT:
                self.player.ActiveSprite(self.playerImageLeftJumping)
            #still
            elif not self.player.moving and self.lastDirection == Direction.RIGHT:
                self.player.ActiveSprite(self.playerImageRightStill)
            elif not self.player.moving and self.lastDirection == Direction.LEFT:
                self.player.ActiveSprite(self.playerImageLeftStill)
            #moving
            elif self.player.moving and self.lastDirection == Direction.RIGHT:
                self.player.ActiveSprite(self.playerImageRightMoving)
            elif self.player.moving and self.lastDirection == Direction.LEFT:
                self.player.ActiveSprite(self.playerImageLeftMoving)




            #death
            if self.player.rect.top > self.screen_height:
                engineOn = False
                #dead
                gameState = GameState.get_instance()
                gameState.state = State.DEATH

            #draw
            self.draw(self.objects, self.backgroundManager)
            

    def draw(self, objects, bgManager):
        # Clear the screen
        self.screen.fill("black")

        bgManager.draw(self.screen)
        objects.draw(self.screen)
        

        # Update the display
        pygame.display.update()



    
