import pygame
import time
from assets.objects.player import Player, Direction
from assets.objects.platform import Platform
from core.stateManager import State, GameState
from core.helpers.collideHelper import CollisionDetection
from core.helpers.backgroundManager import BackgroundManager
from core.helpers.backgroundLayer import BackgroundLayer
from assets.objects.endPlatform import EndPlatform
from assets.objects.startPlatform import StartPlatform

class Engine():
    def __init__(self, screen, currentLevel, screen_width, screen_height , playerImages:list, platformImages:list, parallaxImages:list):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.currentLevel = currentLevel
        self.ticks = 1
        self.font = pygame.font.Font(None, 36)
        self.bg_color = (255, 255, 255)
        self.startingX = (screen_width / 2) - 100
        self.endingX = 6000
        self.startingY = 400
        self.startingY_StartPlatform = 200
        self.startingXPlayer = (screen_width / 2) - 50
        self.startingYPlayer = self.startingY - 64
        self.playerImages = playerImages
        self.platformImages = platformImages
        self.player = Player(self.startingXPlayer, self.startingYPlayer, self.playerImages[1])

        self.startPlatform = StartPlatform(self.startingX, self.startingY_StartPlatform, self.platformImages[0])
        self.platformSmall = Platform(self.startingX + 1300, self.startingY, self.platformImages[1])
        self.endPlatform = EndPlatform(self.endingX, self.startingY, self.platformImages[2])

        self.platforms = [self.startPlatform, self.platformSmall, self.endPlatform]

        self.noMovement = False

        self.parallaxImages = parallaxImages

        self.cloudSpeed = 1
        self.backgroundSpeed = 1
 
        #background
        self.background_0 = BackgroundLayer(0,0,self.screen, self.screen_width, self.screen_height, self.screen_width, self.parallaxImages[0], 0)

        #parallax foregound
        self.backgroundManagerCloud = BackgroundManager(self.player, self.screen, 200, self.screen_width, self.parallaxImages[1], self.cloudSpeed)
        self.backgroundManagerHill = BackgroundManager(self.player, self.screen,  self.screen_height, self.screen_width, self.parallaxImages[2], 2)
        self.backgroundManagerMtn = BackgroundManager(self.player, self.screen,  self.screen_height, self.screen_width, self.parallaxImages[3], 3)
        

        self.playerImageLeftStill = self.playerImages[0]
        self.playerImageRightStill = self.playerImages[1]
        self.playerImageLeftMoving = self.playerImages[2] 
        self.playerImageRightMoving = self.playerImages[3]
        self.playerImageLeftJumping = self.playerImages[4] 
        self.playerImageRightJumping = self.playerImages[5]
        self.lastDirection = Direction.RIGHT
        
        
        self.playerOnPlatform = False
        self.noMovement = False
        self.playerWin = False

        self.collisionDetect = CollisionDetection()
        
        

    def reset(self):
        self.player = Player(self.startingXPlayer, self.startingYPlayer, self.playerImages[1])

        
        self.startPlatform = StartPlatform(self.startingX, self.startingY_StartPlatform, self.platformImages[0])
        self.platformSmall = Platform(self.startingX + 1300, self.startingY, self.platformImages[1])
        self.platformSmall2 = Platform(self.startingX + 2000, self.startingY, self.platformImages[1])
        self.platformSmall3 = Platform(self.startingX + 2700, self.startingY, self.platformImages[1])
        self.platformSmall4 = Platform(self.startingX + 3400, self.startingY, self.platformImages[1])
        self.platformSmall5 = Platform(self.startingX + 4100, self.startingY, self.platformImages[1])
        self.platformSmall6 = Platform(self.startingX + 4800, self.startingY, self.platformImages[1])
        self.endPlatform = EndPlatform(self.endingX, self.startingY, self.platformImages[2])

        self.platforms = [self.startPlatform, self.platformSmall, self.platformSmall2, self.platformSmall3, 
                          self.platformSmall4, self.platformSmall5, self.platformSmall6, self.endPlatform]
        
        #background
        self.background_0 = BackgroundLayer(0,0,self.screen, self.screen_width, self.screen_height, self.screen_width, self.parallaxImages[0], 0)

        #parallax foregound
        self.backgroundManagerCloud = BackgroundManager(self.player, self.screen, 200, self.screen_width, self.parallaxImages[1], self.cloudSpeed)
        self.backgroundManagerHill = BackgroundManager(self.player, self.screen,  self.screen_height, self.screen_width, self.parallaxImages[2], 2)
        self.backgroundManagerMtn = BackgroundManager(self.player, self.screen,  self.screen_height, self.screen_width, self.parallaxImages[3], 3)
        

        self.playerOnPlatform = False
        self.noMovement = False
        self.playerWin = False
        



    
    def runGame(self):
        self.ticks = 1
        engineOn = True
        self.objects = pygame.sprite.Group()
        customDetect = CollisionDetection()

        #backgrounds
        self.objects.add(self.background_0)
        for bg in self.backgroundManagerCloud.backgrounds:
            self.objects.add(bg)
        for bg in self.backgroundManagerHill.backgrounds:
            self.objects.add(bg)
        for bg in self.backgroundManagerMtn.backgrounds:
            self.objects.add(bg)
       
        #platforms
        platform_group = pygame.sprite.Group()
        for platform in self.platforms:
            platform_group.add(platform)
            self.objects.add(platform)

        #player
        self.objects.add(self.player)
        last_time = 0
        while engineOn:
            self.ticks += 1

            # Calculate the time that has passed since the last frame
            current_time = pygame.time.get_ticks()
            delta_time = current_time - last_time
            last_time = current_time
            print(f"Current Time: {current_time} Delta Time: {delta_time} Last Time: {current_time}")
            
            # Calculate the distance that the clouds should move this frame
            cloud_distance = self.cloudSpeed * delta_time / 1000
            bg_distance = self.backgroundSpeed * delta_time / 1000
            print(f"Cloud Speed/Dist: {cloud_distance} BG Speed/Dist: {bg_distance}")

            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE and not self.player.jumping and not self.player.falling:
                     #JUMPING
                    self.player.jumping = True
           

            self.playerOnPlatform = False       
            self.playerWin = False
            #collision (on platform)        
            for platform in self.platforms:            
                if self.collisionDetect.check_collisionTop(self.player.rect, platform.collideRect):
                    self.playerOnPlatform = True          
                    if platform is self.endPlatform:
                        self.playerWin = True        
                    break
            
            self.noMovement = False
            #collision (left/right)
            for platform in self.platforms:            
                if self.collisionDetect.check_collisionRight(self.player.rect, platform.collideRect):
                    self.noMovement = True
                    break
                if self.collisionDetect.check_collisionLeft(self.player.rect, platform.collideRect):
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
                self.backgroundManagerHill.update(Direction.RIGHT, self.noMovement, bg_distance)                   
                self.backgroundManagerMtn.update(Direction.RIGHT, self.noMovement, bg_distance)  
                for platform in self.platforms:                           
                    platform.update(self.playerOnPlatform, self.player.rect, Direction.RIGHT, self.noMovement)                
            #MOVING LEFT
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.Action(True, Direction.LEFT)
                self.lastDirection = Direction.LEFT
                self.backgroundManagerHill.update(Direction.LEFT, self.noMovement, bg_distance)    
                self.backgroundManagerMtn.update(Direction.LEFT, self.noMovement, bg_distance)    
                for platform in self.platforms:                         
                    platform.update(self.playerOnPlatform, self.player.rect, Direction.LEFT, self.noMovement)                             
            #STILL
            else:
                if self.lastDirection == Direction.RIGHT:
                    self.player.Action(False, Direction.RIGHT)
                elif self.lastDirection == Direction.LEFT:
                    self.player.Action(False, Direction.LEFT)


        #environment
            self.backgroundManagerCloud.update(Direction.LEFT, self.noMovement, cloud_distance) 


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
            
            self.draw(self.objects)

            if self.playerWin == True:
                engineOn = False
                #win
                gameState = GameState.get_instance()
                gameState.state = State.WIN

            
            

    def draw(self, objects):
        # Clear the screen
        self.screen.fill("black")

        objects.draw(self.screen)
        

        # Update the display
        pygame.display.update()



    
