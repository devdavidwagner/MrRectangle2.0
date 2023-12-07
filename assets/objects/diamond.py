import pygame
from assets.objects.player import Direction
from core.helpers.collideHelper import CollisionDetection

class Diamond(pygame.sprite.Sprite):
    def __init__(self, x, y, image, images):
        super().__init__()
        self.image = pygame.transform.scale(image, (100, 100))
        self.images = images
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.customDetect = CollisionDetection()
        self.collideRect = pygame.Rect(x,  y, self.rect.width, self.rect.height)
        self.collideRect.center = (x,y)
        self.score = 800
        self.font = pygame.font.Font(None, 55)
        self.scoreTicks = 0

        self.text_rect = self.rect
        self.text_rect.center = (x, y)
        self.collided = False
        self.collidedTicks = 0 
        self.eaten = False
        self.addedScore = False

    def update(self,direction = Direction.RIGHT, noMovement = False):
        if not noMovement:
            self.move(direction)

      
    def move(self, direction):       
        if direction == Direction.LEFT:
            self.rect.x += self.speed 
            self.collideRect.x += self.speed
        if direction == Direction.RIGHT:
            self.rect.x -= self.speed
            self.collideRect.x -= self.speed

    def display_fruity_score(self,screen):
        if self.collided:        
            self.collidedTicks += 1
            print(str(self.collidedTicks))
            if self.scoreTicks < 50:
                self.ActiveSprite(self.images[1])
            
            if self.scoreTicks < 100 and self.scoreTicks > 50:
                self.ActiveSprite(self.images[2])

            if self.scoreTicks > 100:
                self.ActiveSprite(self.images[3])

            if self.scoreTicks < 250:
                text = self.font.render(f"+{self.score}", True, "GREEN")
                if self.scoreTicks % 4 == 2:
                    text = self.font.render(f"+{self.score}!", True, "RED")
                self.scoreTicks += 1
                screen.blit(text, self.text_rect)
            else:
                self.collided = False
                self.eaten = True

    def draw_collision_rect(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.collideRect, 2)            

    def ActiveSprite(self, image):
        self.image =  pygame.transform.scale(image, (100, 100))