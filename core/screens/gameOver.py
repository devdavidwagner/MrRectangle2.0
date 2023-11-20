import pygame
from core.stateManager import State, GameState
from core.helpers.soundManager import SoundManager

class GameOver:
    def __init__(self, screen_width, screen_height, deadPlayerImg, background):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 40) 
        self.scoreFont =  pygame.font.Font(None, 60)  
        self.death_text = self.scoreFont.render("GAME OVER", True, (255, 0, 0))
        self.restart_text = self.font.render("PRESS ANY KEY TO RETURN TO MAIN MENU", True, (255, 255, 255))
       
        self.death_text_rect = self.death_text.get_rect(center=(screen_width/2, screen_height/2 - 50))
        self.restart_text_rect = self.restart_text.get_rect(center=(screen_width/2, screen_height/2 + 50))
        self.deadPlayerImg = deadPlayerImg
        self.scaledImg = pygame.transform.scale(self.deadPlayerImg, (100, 80))
        self.soundManager = SoundManager()
        self.soundManager.load_sound_effect("Death", "assets\sounds\Died.wav")
        self.soundPlayed = False
        self.background = background
        
    def display(self, screen, score):
        scoreText = self.scoreFont.render("SCORE: " + str(score), True, (0, 255, 0))
        score_text_rect = scoreText.get_rect()
        score_text_rect.x = (self.screen_width / 2) - 100
        score_text_rect.y = (self.screen_height / 2 ) - 200
        
        screen.blit(self.background, (0,0))
        screen.blit(self.death_text, self.death_text_rect)
        screen.blit(self.restart_text, self.restart_text_rect)
        screen.blit(scoreText, score_text_rect)
        screen.blit(self.scaledImg, ((self.screen_width/2) - 50, (self.screen_height / 2) - 40))
        if not self.soundPlayed:
            self.soundManager.play_sound_effect("Death", 5)
            self.soundPlayed = True
     
        pygame.display.update()

    
    
    def handle_event(self, event, screen):
        currentState = GameState.get_instance()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.soundPlayed = False
                currentState.state = State.MENU


