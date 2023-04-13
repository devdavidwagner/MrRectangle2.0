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
        self.startingXPlayer = (screen_width / 2) - 50
        self.startingYPlayer = 0
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
        self.platforms = [self.platform, self.platformSmall]

    
    def runGame(self):
        ticks = 0
        engineOn = True
        self.objects = pygame.sprite.Group()
        self.objects.add(self.player)
        for platform in self.platforms:
            self.objects.add(platform)

        while engineOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
    
                    
            ticks += 1

             
            #collision
            currentPlatform = None
            onPlatform = False
            for platform in self.platforms:
                if pygame.rect.Rect.colliderect(self.player.rectCollide, platform.rectCollide):
                    self.player.Action(False, None, False)  #on platform                            
                    onPlatform = True
                    currentPlatform = platform
                    print("PLAYER ON PLATFORM")
                    break



            if not onPlatform:
                self.player.Action(False, None, True) #falling
                print("PLAYER FALLING")
            else:
                self.player.falling = False

            keys = pygame.key.get_pressed()

        #KEYS/ACTIONS
            #JUMPING
            if keys[pygame.K_SPACE] and self.lastDirection == Direction.RIGHT:
                self.player.Action(False, Direction.RIGHT, False, True)
            
            elif keys[pygame.K_SPACE] and self.lastDirection == Direction.LEFT:
                self.player.Action(False, Direction.LEFT, False, True)


            
            #MOVING RIGHT
            stuck = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.Action(True, Direction.RIGHT)
                self.lastDirection = Direction.RIGHT

                
                for platform in self.platforms:   
                    if onPlatform: 
                        platform.Move(self.player.SPEED, Direction.RIGHT)
                    elif not onPlatform and not pygame.sprite.collide_rect(self.player, platform) and not stuck:
                        platform.Move(self.player.SPEED, Direction.RIGHT) 
                    else:
                        stuck = True
                      
                
            
                    
            #MOVING LEFT
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.Action(True, Direction.LEFT)
                self.lastDirection = Direction.LEFT
           
                for platform in self.platforms:  
                    if onPlatform:
                        platform.Move(self.player.SPEED, Direction.LEFT)
                    elif not onPlatform and not pygame.sprite.collide_rect(self.player, platform) and not stuck:
                        platform.Move(self.player.SPEED, Direction.LEFT) 
                    else:
                        stuck = True

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


            self.draw(self.objects)
            

    def draw(self, objects):
        # Clear the screen
        self.screen.fill("black")

        objects.draw(self.screen)

        # Update the display
        pygame.display.update()



    
