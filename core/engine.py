import pygame
from assets.sprites.objects.rectangle import Rectangle, Direction
from assets.sprites.objects.platform import Platform
from core.stateManager import State, GameState

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
        self.playerImages = playerImages
        self.platformImages = platformImages
        self.player = Rectangle(self.startingX, self.startingY, self.playerImages[1])
        self.platform = Platform(0, self.startingY + self.player.rect.height, self.platformImages[0])


        self.playerImageLeftStill = self.playerImages[0]
        self.playerImageRightStill = self.playerImages[1]
        self.playerImageLeftMoving = self.playerImages[2] 
        self.playerImageRightMoving = self.playerImages[3]
        self.playerImageLeftJumping = self.playerImages[4] 
        self.playerImageRightJumping = self.playerImages[5]
        self.lastDirection = Direction.RIGHT
        
        

    def reset(self):
        self.player = Rectangle(self.startingX, self.startingY, self.playerImages[1])
        self.platform = Platform(0, self.startingY + self.player.rect.height, self.platformImages[0])

    
    def runGame(self):
        ticks = 0
        engineOn = True
        self.objects = pygame.sprite.Group()
        self.objects.add(self.player)
        self.objects.add(self.platform)

        while engineOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
            ticks += 1

             
            #collision
            playerOffPlat = True
            if pygame.sprite.collide_rect(self.player, self.platform) and self.platform.rect.top > self.player.rect.y:
                self.player.Action(False, None, False)  #on platform
                print("PLAYER ON PLATFORM")
            else :
                self.player.Action(False, None, True) #falling
                print("PLAYER FALLING")



            leftLimitUnderY = self.player.rect.left
            rightLimitUnderY = self.player.rect.left

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.player.rect.right < self.screen_width:
                self.player.Action(True, Direction.RIGHT)
                self.lastDirection = Direction.RIGHT
                self.player.ActiveSprite(self.playerImageRightMoving)          
                if self.platform.rect.left < rightLimitUnderY:
                    self.platform.Move(self.player.SPEED, Direction.RIGHT)
                elif pygame.sprite.collide_rect(self.player, self.platform):
                    self.platform.Move(self.player.SPEED, Direction.RIGHT)
                    
                
            elif keys[pygame.K_LEFT] or keys[pygame.K_a] and self.player.rect.left > 0:
                self.player.Action(True, Direction.LEFT)
                self.lastDirection = Direction.LEFT
                self.player.ActiveSprite(self.playerImageLeftMoving)     

                if  self.platform.rect.right < leftLimitUnderY:
                    self.platform.Move(self.player.SPEED, Direction.LEFT)
                elif pygame.sprite.collide_rect(self.player, self.platform):
                    self.platform.Move(self.player.SPEED, Direction.LEFT)
            else:
                if self.lastDirection == Direction.RIGHT:
                        self.player.ActiveSprite(self.playerImageRightStill) 
                elif self.lastDirection == Direction.LEFT:
                        self.player.ActiveSprite(self.playerImageLeftStill) 


            if keys[pygame.K_SPACE] and self.lastDirection == Direction.RIGHT:
                self.player.ActiveSprite(self.playerImageRightJumping)
                self.player.Action(True, Direction.RIGHT, False, True)
            
            elif keys[pygame.K_SPACE] and self.lastDirection == Direction.LEFT:
                self.player.ActiveSprite(self.playerImageLeftJumping)  
                self.player.Action(True, Direction.LEFT, False, True)





            #death
            if self.player.rect.top > self.screen_height:
                engineOn = False
                #dead
                gameState = GameState.get_instance()
                gameState.state = State.DEATH


            self.draw(self.objects)
            

    def draw(self, objects):
        # Clear the screen
        self.screen.fill("black")

        objects.draw(self.screen)

        # Update the display
        pygame.display.update()



    
