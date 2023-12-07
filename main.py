# Import standard modules.
import sys
import os
# Import non-standard modules.
import pygame
from pygame.locals import *

from core.stateManager import State, GameState
from core.screens.menu import Menu
from core.screens.levelManager import LevelManager, Level
from core.screens.death import Death
from core.screens.gameOver import GameOver
from core.screens.win import Win

def update(dt):
  """
  Update game. Called once per frame.
  dt is the amount of time passed since last frame.
  If you want to have constant apparent movement no matter your framerate,
  what you can do is something like
  
  x += v * dt
  
  and this will scale your velocity based on time. Extend as necessary."""
  
  # Go through events that are passed to the script by the window.
  for event in pygame.event.get():
    # We need to handle these events. Initially the only one you'll want to care
    # about is the QUIT event, because if you don't handle it, your game will crash
    # whenever someone tries to exit.
    if event.type == QUIT:
      pygame.quit() # Opposite of pygame.init
      sys.exit() # Not including this line crashes the script on Windows. Possibly
      # on other operating systems too, but I don't know for sure.
    # Handle other events as you wish.
 
def draw(screen):
  """
  Draw things to the window. Called once per frame.
  """
  screen.fill((0, 0, 0)) # Fill the screen with black.
  
  # Redraw screen here.
  
  # Flip the display so that the things we drew actually show up.
  pygame.display.flip()

def load_high_score():
        try:
            with open("high_score.txt", "r") as file:
                high_score_str = file.read()
                if high_score_str.isdigit():
                    high_score = int(high_score_str)
                    print("High score loaded successfully:", high_score)
                    return high_score
                else:
                    print("Invalid high score format in the file.")
                    return None
        except IOError as e:
            print("Error loading high score:", str(e))
            return None
        
def save_high_score():
  try:        
      gameState = GameState.get_instance()
      if gameState.check_high_score_updated() == False:
        highScore = load_high_score()
        currentScore = gameState.get_score()
        if(currentScore > highScore):
          with open("high_score.txt", "w") as file:         
              file.write(str(gameState.get_score()))
              print("High score saved successfully.")
        else:
          print("Not a high score.")

        gameState.set_high_score_updated(True)
  except IOError as e:
      print("Error saving high score:", str(e))
 
def runPyGame():
  # Initialise PyGame.
  pygame.init()
  
  # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
  fps = 60.0
  fpsClock = pygame.time.Clock()
  
  # Set up the window.
  screen_width = 800
  screen_height = 600
  screen = pygame.display.set_mode((screen_width, screen_height))
  
  # Main game loop.
  dt = 1/fps # dt is the time since last frame.
  menu = Menu(screen_width, screen_height, 500,100)

  currentLevel = Level.ONE
  
  deadImg = pygame.image.load("assets\sprites\dead.png").convert_alpha()
  deathBackground = pygame.image.load("assets\sprites\deathBackground.png").convert_alpha()
  deathScreen = Death(screen_width, screen_height, deadImg, deathBackground)

  gameOverBackground = pygame.image.load("assets\sprites\gameOverBackground.png").convert_alpha()
  gameOverScreen = GameOver(screen_width, screen_height, deadImg, gameOverBackground)
  winImg = pygame.image.load("assets\sprites\win.png").convert_alpha()
  winBg = pygame.image.load("assets\sprites\para0.png").convert_alpha()
  winScreen = Win(screen_width, screen_height,winImg, winBg)

  isAlive = True
  gameState = GameState.get_instance()
  gameState.state = State.MENU
  switchLevel = False
  
  while True: # Loop forever!
    if gameState.state == State.MENU:
      #run menu  
      gameState.resetLives()
      menu.draw(screen)

    if gameState.state == State.GAME:
      #run level 1  
      gameState.set_high_score_updated(False)
      levelMan = LevelManager(currentLevel, screen, screen_width, screen_height)
      levelMan.runLevel()
      switchLevel = True

    
    if gameState.state == State.DEATH:
      deathScreen.display(screen, gameState.get_score())
      deathScreen.handle_event(event,screen)

    if gameState.state == State.GAME_OVER:
      save_high_score()
      gameState.set_score(0)
      gameState.resetLives()
      gameState.resetLevels()
      gameOverScreen.display(screen, gameState.get_score())
      gameOverScreen.handle_event(event,screen)

    if gameState.state == State.WIN:
      winScreen.display(screen, gameState.get_score())
      winScreen.handle_event(event,screen)      
      if switchLevel:
        gameState.next_level()
        switchLevel = False

    #events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      if gameState.state == State.MENU:
          menu.handle_event(event, screen)

    
    dt = fpsClock.tick(fps)


