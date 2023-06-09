import pygame
from core.stateManager import State, GameState
from core.helpers.soundManager import SoundManager

class Win:
    def __init__(self, screen_width, screen_height, winImg, winBg):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.live_text = self.font.render("MR. RECTANGLE LIVES!", True, (124,252,0))
        self.cont_text = self.font.render("PRESS ANY KEY TO CONTINUE TO NEXT LEVEL", True, (255, 255, 255))
        self.live_text_rect = self.live_text.get_rect(center=(screen_width/2, (screen_height/2) - 150))
        self.cont_text_rect = self.cont_text.get_rect(center=(screen_width/2, (screen_height/2) + 50))
        self.winImg = winImg
        self.winBg = winBg
        self.soundManager = SoundManager()
        self.soundManager.load_sound_effect("Win", "assets\sounds\Win.wav")
        self.soundPlayed = False
    
    def display(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.winBg, (0,0))
        screen.blit(self.cont_text, self.cont_text_rect)
        screen.blit(self.winImg, ((self.screen_width/2) - 250, (self.screen_height / 2)  - 200))
        screen.blit(self.live_text, self.live_text_rect)
        if not self.soundPlayed:
            self.soundManager.play_sound_effect("Win", 5)
            self.soundPlayed = True
        pygame.display.update()

    
    
    def handle_event(self, event, screen):
        currentState = GameState.get_instance()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                currentState.state = State.GAME
                self.soundPlayed = False


