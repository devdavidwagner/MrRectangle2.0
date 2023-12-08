import pygame
from enum import Enum
from core.stateManager import GameState

class Direction(Enum):
    LEFT = 1
    RIGHT = 2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, playerImages, score, playerImagesUpgrade1):
        super().__init__()
        self.image = image 
        self.rect = self.image.get_bounding_rect()
        self.rect.height = 80
        self.rect.width = 40
        self.rect.center = (x, y)
        self.playerImages = playerImages
        self.moving = False
        self.jumping = False
        self.shooting = False
        self.fallAfterJump = False
        self.falling = False
        self.ticksJumping = 1
        self.ticksFallingAfterJump = 1
        self.ticks = 1
        self.shootingTicks = 1
        self.projectilesFired = 0
        self.SPEED = 4
        self.GRAVITY = 2
        self.JUMP_SPEED = 5
        self.JUMP_LENGTH_IN_TICKS = 30
        self.FALL_LENGTH_IN_TICKS = 40
        self.SHOOTING_LENGTH_IN_TICKS = 600
        self.dying = False
        self.dead = False
        self.dyingTicks = 0
        self.splatSet = False
        self.score = score
        self.prevScore = 0
        self.scoreAddedTo = False
        self.showAddTicks = 0
        self.diff = 0
        pygame.font.init()
        self.fontAdded = pygame.font.Font(None, 55)
        self.font = pygame.font.Font(None, 36)

        self.ducking = True
        self.duckingTicks = 0
        self.ducked = False
        self.yBeforeDuck = self.rect.x

        self.fallingTicks = 0
        self.jumpUsed = False

        self.jumpBoost = False
        self.jumpBoostTicks = 0
        self.ticksAfterBoost = 0
        self.fallAfterBoost = False
        self.boxColor = (29,118,76)  # light green
        gameState = GameState.get_instance()
        self.playerLives = gameState.get_player_life()
        self.life_image = pygame.image.load("assets\sprites\life.png")  # Replace with the actual path to your "life.png" image
        self.life_image = pygame.transform.scale(self.life_image, (50, 50))
        self.life_rect = pygame.Rect(350, 10, 200, 35)

        self.life_box = pygame.Surface((self.life_rect.width, self.life_rect.height))
        self.life_box.set_alpha(200)  # Set the alpha value to control the transparency (0 is fully transparent, 255 is fully opaque)
        self.life_box.fill(self.boxColor)  # Set the color of the box 

        self.upgradeLVL = 0
        self.upgrading = False
        self.upgradeTicks = 0 

        self.playerImagesUpgrade1 = playerImagesUpgrade1   
    
    def AddToScore(self, add):
        self.score += add 

    def Upgrade(self):
        self.upgradeLVL +=1
        self.upgrading = True

    def Hit(self):
        self.dying = True

    def InstaDie(self):
        if self.upgradeLVL == 0:
            self.ActiveSprite(self.playerImages[17])
        if self.upgradeLVL > 0:
            self.ActiveSprite(self.playerImagesUpgrade1[17])
        self.dyingTicks = 0
        self.dead = True

    def Dying(self):
        self.moving = False
        self.falling = False
        self.shooting = False
        self.dyingTicks += 1
        if self.dyingTicks > 0 and len(self.playerImages) > 0:
            if self.upgradeLVL == 0:
                self.ActiveSprite(self.playerImages[20])
            if self.upgradeLVL > 0:
                self.ActiveSprite(self.playerImagesUpgrade1[20])
        if self.dyingTicks > 120 and len(self.playerImages) > 0:
            if self.upgradeLVL == 0:
                self.ActiveSprite(self.playerImages[21])
            if self.upgradeLVL > 0:
                self.ActiveSprite(self.playerImagesUpgrade1[21])
        if self.dyingTicks > 240 and len(self.playerImages)> 0:
            if self.upgradeLVL == 0:
                self.ActiveSprite(self.playerImages[22])
            if self.upgradeLVL > 0:
                self.ActiveSprite(self.playerImagesUpgrade1[22])
         

        if self.dyingTicks > 360:
            if self.upgradeLVL == 0:
                self.ActiveSprite(self.playerImages[20])
            if self.upgradeLVL > 0:
                self.ActiveSprite(self.playerImagesUpgrade1[20])
            self.dyingTicks = 0
            self.dead = True
            self.dying = False
            self.upgradeLVL = 0


    def draw(self, screen):
        # Create a text surface with the player's score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))  # You can change the color (here, white) as needed

        # Get the rectangle that represents the text surface
        score_rect = score_text.get_rect()
        score_rect.width = score_rect.width  * 2
        score_rect.height = score_rect.height * 1.5
        # Set the position of the text (top-left corner)
        score_rect.topleft = (10, 10)  # Adjust the position as needed       
        # Create a translucent box behind the score
        score_box = pygame.Surface((score_rect.width, score_rect.height))
        score_box.set_alpha(200)  # Set the alpha value to control the transparency (0 is fully transparent, 255 is fully opaque)
        score_box.fill(self.boxColor)  # Set the color of the box (gray in this case)
        screen.blit(score_box, score_rect.topleft)
        # Blit the text surface onto the screen
        screen.blit(score_text, (score_rect.x + score_rect.width /4, score_rect.y ))    
        if self.upgrading:
            self.upgradeTicks += 1
            if self.upgradeTicks < 25:
                screen.blit(pygame.transform.scale(self.playerImages[29], (100,100)), (self.rect.left - self.rect.width /2, self.rect.y))
            elif self.upgradeTicks >= 25 and self.upgradeTicks < 50:
                screen.blit(pygame.transform.scale(self.playerImages[30], (100,100)), (self.rect.left - self.rect.width /2, self.rect.y))
            elif self.upgradeTicks >= 50 and self.upgradeTicks < 75:
                screen.blit(pygame.transform.scale(self.playerImages[31], (100,100)), (self.rect.left - self.rect.width /2, self.rect.y))
            elif self.upgradeTicks >= 75 and self.upgradeTicks < 100:
                screen.blit(pygame.transform.scale(self.playerImages[31], (100,100)), (self.rect.left - self.rect.width /2, self.rect.y))
            else:
                self.upgrading = False
                self.upgradeTicks = 0
                
        if self.prevScore != self.score and not self.scoreAddedTo:
            self.diff = self.score - self.prevScore
            self.diff = abs(self.diff)
            self.scoreAddedTo = True

        if self.scoreAddedTo:
            self.showAddTicks += 1
            add_score_text = self.fontAdded.render(f"+ {self.diff} !", True,  (0, 255, 0)) 
                # Get the rectangle that represents the text surface
            add_score_rect = add_score_text.get_rect()
            add_score_rect.width = add_score_rect.width  * 2
            add_score_rect.height = add_score_rect.height * 1.5
            add_score_rect.center = (100, 60)

            if self.showAddTicks < 100:
                print("add to score showing")
                screen.blit(add_score_text, (add_score_rect.x + add_score_rect.width /4, add_score_rect.y ))
            else:
                self.showAddTicks = 0
                self.scoreAddedTo = False
          
        self.prevScore = self.score

        #lives
        life_text = self.font.render(f"Lives:", True, (255, 255, 255))  # You can change the color (here, white) as needed
        screen.blit(self.life_box, (self.life_rect.x , self.life_rect.y ))
        screen.blit(life_text, (self.life_rect.x , self.life_rect.y ))
        
        for i in range(self.playerLives):
            screen.blit(self.life_image, (self.life_rect.x + life_text.get_width() + (i * 40), 0))  # Adjust the spacing as needed
    
    def JumpBoost(self):
        self.jumpBoostTicks += 1
        if self.jumpBoostTicks < 100:        
            self.rect.y -= 5     
            print("JUMP BOOST") 
        else:
            self.jumpBoost = False
            self.jumpBoostTicks = 0 

        

    def Action(self, moving, direction = Direction.RIGHT, falling = False, initJump = False, shooting = False, ducking = False, jumpBoost = False):  
        self.moving = moving
        self.falling = falling
        self.shooting = shooting
        self.ducking = ducking
        self.ticks += 1

        if not ducking:
            self.yBeforeDuck = self.rect.y
        
        if shooting:
            self.shootingTicks += 1
        
            
        if initJump == True and not self.jumping and not self.falling:
            self.jumping = initJump
                   
        if self.falling and not self.jumping or self.fallAfterJump:
            self.rect.y += self.GRAVITY
           

        if self.ticks % 20 == 1:
            
            if self.jumping == True:
                self.JUMP_SPEED = self.JUMP_SPEED + 0.4
                self.ticksJumping += 1
                self.rect.y -= self.JUMP_SPEED - self.GRAVITY

            if self.JUMP_LENGTH_IN_TICKS % self.ticksJumping == 1:
                self.jumping = False
                self.fallAfterJump = True
                self.ticksJumping = 1

            if  self.fallAfterJump:
                self.JUMP_SPEED = 6
                self.ticksFallingAfterJump += 1
                self.rect.y += self.GRAVITY

            if self.FALL_LENGTH_IN_TICKS % self.ticksFallingAfterJump  == 1:
                self.fallAfterJump = False
                self.ticksFallingAfterJump = 1
    
    def Duck(self):
        pass

    def EndDuck(self):
        pass

    def ActiveSprite(self, image):
        self.image =  pygame.transform.scale(image, (40, 80))

    def ActiveSpriteAndResize(self, image, width = 40, height = 80):
        self.image =  pygame.transform.scale(image, (width, height))
        self.rect.height = height
        
    def draw_collision_rect(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)


