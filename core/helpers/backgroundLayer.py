import pygame
from assets.objects.player import Direction

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
        self.ticks = 1

    def move(self, direction, object_distance_speed):       
        if direction == Direction.LEFT:
            self.rect.x += object_distance_speed
        if direction == Direction.RIGHT:
            self.rect.x -= object_distance_speed


    def update(self, direction, noMovement, object_distance_speed):
        if not noMovement:
            self.move(direction, object_distance_speed)


   
        

