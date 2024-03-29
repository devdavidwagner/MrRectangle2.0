import pygame
from assets.objects.player import Direction
from core.helpers.collideHelper import CollisionDetection

class JumpBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, image: pygame.image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.customDetect = CollisionDetection()
        self.collideRect =  pygame.Rect(x,  y, self.rect.width, self.rect.height)
        self.hit = False
        self.activateSprite = 1
    
    def move(self, direction):       
        if direction == Direction.LEFT:
            self.rect.x += self.speed
            self.collideRect.x += self.speed
        if direction == Direction.RIGHT:
            self.rect.x -= self.speed
            self.collideRect.x -= self.speed

    def update(self,direction = Direction.RIGHT, noMovement = False):
        if not noMovement:
            self.move(direction)

    def draw_collision_rect(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.collideRect, 2)

    def ActiveSprite(self, image):
        self.image =  image