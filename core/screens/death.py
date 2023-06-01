import pygame
from core.stateManager import State, GameState

class Death:
    def __init__(self, screen_width, screen_height, deadPlayerImg):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.death_text = self.font.render("RIP MR. RECTANGLE", True, (255, 0, 0))
        self.restart_text = self.font.render("PRESS ANY KEY TO RESTART", True, (255, 255, 255))
        self.death_text_rect = self.death_text.get_rect(center=(screen_width/2, screen_height/2 - 50))
        self.restart_text_rect = self.restart_text.get_rect(center=(screen_width/2, screen_height/2 + 50))
        self.deadPlayerImg = deadPlayerImg
        self.scaledImg = pygame.transform.scale(self.deadPlayerImg, (100, 80))
    
    def display(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.death_text, self.death_text_rect)
        screen.blit(self.restart_text, self.restart_text_rect)
        screen.blit(self.scaledImg, ((self.screen_width/2) - 50, (self.screen_height / 2) - 40))
        pygame.display.update()

    
    
    def handle_event(self, event, screen):
        currentState = GameState.get_instance()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                currentState.state = State.GAME


