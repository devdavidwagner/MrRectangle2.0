import pygame
from assets.objects.player import Direction
from core.helpers.collideHelper import CollisionDetection

class StartPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, image: pygame.image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.customDetect = CollisionDetection()

        self.collideRect = pygame.Rect(x, y * 2, 800, 200)

    def move(self, direction):       
        if direction == Direction.LEFT:
            self.rect.x += self.speed
            self.collideRect.x += self.speed
        if direction == Direction.RIGHT:
            self.rect.x -= self.speed
            self.collideRect.x -= self.speed

    def update(self, onPlatform, playerRect, direction = Direction.RIGHT, noMovement = False):
        if not noMovement:
            self.move(direction)