import pygame
from assets.sprites.objects.rectangle import Rectangle, Direction
from assets.sprites.objects.platform import Platform
from core.stateManager import State, GameState
from core.helpers.collideHelper import CollisionDetection

class Engine():
    def __init__(self, screen, currentLevel, screen_width, screen_height , playerImages:list, platformImages:list):
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


        self.playerImageLeftStill = self.playerImages[0]
        self.playerImageRightStill = self.playerImages[1]
        self.playerImageLeftMoving = self.playerImages[2] 
        self.playerImageRightMoving = self.playerImages[3]
        self.playerImageLeftJumping = self.playerImages[4] 
        self.playerImageRightJumping = self.playerImages[5]
        self.lastDirection = Direction.RIGHT
        
        

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
        self.objects.add(self.player)
        for platform in self.platforms:
            self.objects.add(platform)


        customDetect = CollisionDetection()
        while engineOn:
            ticks += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE and not self.player.jumping and not self.player.falling:
                     #JUMPING
                    self.player.jumping = True
           
    
                    
           

             
            #collision
            currentPlatformSide = None
            currentPlatform= None
            onPlatform = False
            for platform in self.platforms:
                if customDetect.check_collisionTop(self.player.rect, platform.rect):
                        # Stop the player sprite at the top of the platform sprite
                        self.player.Action(False, None, False, False)  #on platform                            
                        onPlatform = True
                        currentPlatform = platform
                        print("PLAYER ON PLATFORM")
                        break
                
            for platform in self.platforms:
                if customDetect.check_collisionRight(platform.rect, self.player.rect):                    
                        currentPlatformSide = platform
                        print("PLAYER BESIDE PLATFORM")
                        break
                if customDetect.check_collisionLeft(platform.rect, self.player.rect):                         
                        currentPlatformSide = platform
                        print("PLAYER BESIDE PLATFORM")
                        break
   



            if not onPlatform:
                self.player.Action(False, None, True,False) #falling
                print("PLAYER FALLING")
 

            keys = pygame.key.get_pressed()

        #KEYS/ACTIONS     
         #   JUMPING 
            
            if self.player.jumping == True and self.lastDirection == Direction.RIGHT:
                    self.player.Action(True, Direction.RIGHT, False, True)
                
            elif self.player.jumping == True and self.lastDirection == Direction.LEFT:
                    self.player.Action(True, Direction.LEFT, False, True)

            #MOVING RIGHT
            stuck = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.Action(True, Direction.RIGHT)
                self.lastDirection = Direction.RIGHT
              
                
                noMovement = False
                for platform in self.platforms:  
                    if  customDetect.check_collisionRight(self.player.rect, platform.rect) and currentPlatformSide == platform:
                        noMovement = True 
                 
                if not noMovement:
                   for platform in self.platforms: 
                        platform.Move(self.player.SPEED, Direction.RIGHT)
                   
                    
            #MOVING LEFT
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.Action(True, Direction.LEFT)
                self.lastDirection = Direction.LEFT
           
                noMovement = False
                for platform in self.platforms:  
                    if  not onPlatform and customDetect.check_collisionLeft(self.player.rect, platform.rect) and currentPlatformSide == platform:
                        noMovement = True 

                if not noMovement:
                   for platform in self.platforms: 
                        platform.Move(self.player.SPEED, Direction.LEFT)
            
          

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

            if ticks % 20 != 1:
                print("Player: Y " + str(self.player.rect.y) + " , " + " Player: X " + str(self.player.rect.x))
                print("Current Playform: Y " + str(self.platform.rect.y) + " , " + " Platform: X " + str(self.platform.rect.x) + " TOP: " + str(self.platform.rect.top))



            self.draw(self.objects)
            

    def draw(self, objects):
        # Clear the screen
        self.screen.fill("black")

        objects.draw(self.screen)

        # Update the display
        pygame.display.update()



    
