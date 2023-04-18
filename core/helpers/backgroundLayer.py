import pygame
from assets.sprites.objects.rectangle import Direction

#rect 1 = player
#rect 2 = platform/object
class BackgroundLayer(pygame.sprite.Sprite):
    def __init__(self,x,y, screen, width, height, screen_width, image, speed):
        super().__init__()
        self.image =  pygame.transform.scale(image, (width, height)) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen = screen
        self.speed = speed
        self.screen_width = screen_width
        self.rect.topleft = (x,y)

    def move(self, direction):       
        if direction == Direction.LEFT:
            self.rect.x += self.speed
        if direction == Direction.RIGHT:
            self.rect.x -= self.speed

    def update(self, direction, noMovement):
        if not noMovement:
            self.move(direction)


   
        

