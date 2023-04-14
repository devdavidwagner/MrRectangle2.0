import pygame


#rect 1 = player
#rect 2 = platform/object
class CollisionDetection:
    @staticmethod
    def check_collisionTop(rect1:pygame.rect.Rect, rect2:pygame.rect.Rect):
        if  rect1.bottom > rect2.top - (rect1.height * 2) and rect1.left > rect2.left and rect1.right < rect2.right:           
            return True
        else:
            return False
    
    @staticmethod
    def check_collisionLeft(rect1:pygame.rect.Rect, rect2:pygame.rect.Rect):
        if  rect1.bottom > rect2.top and rect1.left <= rect2.right:       
            return True
        else:
            return False
        
    @staticmethod
    def check_collisionRight(rect1:pygame.rect.Rect, rect2:pygame.rect.Rect):
        if  rect1.bottom > rect2.top and rect1.right >= rect2.left:           
            return True
        else:
            return False 