import pygame
import time
from assets.objects.player import Player, Direction
from assets.objects.enemy import Enemy
from assets.objects.platform import Platform
from core.stateManager import State, GameState
from core.helpers.collideHelper import CollisionDetection
from core.helpers.backgroundManager import BackgroundManager
from core.helpers.soundManager import SoundManager
from core.helpers.backgroundLayer import BackgroundLayer
from core.helpers.levelBuilder import LevelBuilder
from assets.objects.endPlatform import EndPlatform
from assets.objects.startPlatform import StartPlatform
from assets.objects.projectile import Projectile
from assets.objects.splat import Splat
from assets.objects.fruit import Fruit

class Engine():
    def __init__(self, screen, currentLevel, screen_width, screen_height , playerImages:list, platformImages:list, parallaxImages:list, enemyImages:list, fruitImages:list, effectImages:list, soundEffects:list):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.currentLevel = currentLevel
        self.ticks = 1
        self.font = pygame.font.Font(None, 36)
        self.bg_color = (255, 255, 255)
        self.startingX = (screen_width / 2) - 100
        self.endingX = 6000
        self.startingY = 200
        self.startingY_StartPlatform = 200
        self.startingXPlayer = (screen_width / 2) + 50
        self.startingYPlayer = self.startingY - 64
        self.playerImages = playerImages
        self.platformImages = platformImages
        self.effectImages = effectImages
        self.player = Player(self.startingXPlayer, self.startingYPlayer, self.playerImages[1], self.playerImages)
        
        self.level_builder = LevelBuilder(currentLevel, screen_width, screen_height, 40)
        self.levelData = self.level_builder.load_level()
       

        self.startPlatform = None
        self.endPlatform = None
        self.platforms = []
        self.enemies = []
        self.fruits = []
        
        self.fruitImages = fruitImages
        self.enemyImages = enemyImages

        self.enemyGroup = []



        
        self.noMovement = False

        self.parallaxImages = parallaxImages

        self.cloudSpeed = 350
        self.backgroundSpeed = 300
        self.backgroundSpeed2 = 250
        #background
        self.background_0 = BackgroundLayer(0,0,self.screen, self.screen_width, self.screen_height, self.screen_width, self.parallaxImages[0], 0)

        #parallax foregound
        self.backgroundManagerCloud = BackgroundManager(self.player, self.screen, 200, self.screen_width, self.parallaxImages[1], self.cloudSpeed)
        self.backgroundManagerHill = BackgroundManager(self.player, self.screen,  self.screen_height, self.screen_width, self.parallaxImages[2], 2)
        self.backgroundManagerMtn = BackgroundManager(self.player, self.screen,  self.screen_height, self.screen_width, self.parallaxImages[3], 3)
        

        self.projectileImage = self.playerImages[10]
        self.projectilesInAir = []

        self.playerImageLeftStill = self.playerImages[0]
        self.playerImageRightStill = self.playerImages[1]
        self.playerImageLeftMoving = self.playerImages[2] 
        self.playerImageRightMoving = self.playerImages[3]
        self.playerImageLeftJumping = self.playerImages[4] 
        self.playerImageRightJumping = self.playerImages[5]
        self.lastDirection = Direction.RIGHT
        
        self.playerOnPlatform = False
        self.noMovement = False
        self.playerWin = False
        self.currentPlatform = None

        self.collisionDetect = CollisionDetection()

        self.soundManager = SoundManager()
        self.soundEffects = soundEffects
        self.startFruitX = 800
        
        self.objects = pygame.sprite.Group()
        self.generateObjects(self.levelData)

        self.ticks = 0
        
    def generateObjects(self, levelData):
        currentCoods = (0,0)
        # Loop through rows
        self.buildPlatform = False
        self.platformWidth = 0

        self.buildStartPlatform = False
        self.startPlatformWidth = 0 

        self.buildEndPlatform = False
        self.endPlatformWidth = 0  
        xCoods = 0

        charWidth = 50
        for row in levelData: #every row is 100px height         
            currentCoods = (currentCoods[0], currentCoods[1] + charWidth)
            xCoods = 0
            print(f"ROW COODS = {currentCoods}")
            for char in row: #every char is x px width  
                xCoods += charWidth                                  
                print(f"CHAR COODS = {xCoods,currentCoods[1]}")
                if self.buildPlatform:
                    self.platformWidth += charWidth
                    print(f"Build Platform Width = {self.platformWidth}")
                if char == '-':
                    if self.buildStartPlatform:
                        self.buildStartPlatform = False
                        self.startPlatform = StartPlatform(xCoods, currentCoods[1], self.platformImages[0])                    
                        print(f"Start Platform Built and Added")     
                        self.platforms.append(self.startPlatform)
                    if self.buildEndPlatform:
                        self.buildEndPlatform = False
                        self.endPlatform = EndPlatform(xCoods, currentCoods[1], self.platformImages[3])
                        print(f"End Platform Built and Added at: {xCoods}")   
                        self.platforms.append(self.endPlatform)
                elif char == '*': #fruit
                    newFruit = Fruit(xCoods, currentCoods[1], self.fruitImages[0], self.fruitImages)
                    self.fruits.append(newFruit)
                elif char == '<': #start lvl platform
                    if self.buildStartPlatform:
                        self.startPlatformWidth += charWidth
                        print(f"Start Platform Width = {self.platformWidth}")
                    else:
                        self.buildStartPlatform = True
                elif char == '>': #end lvl platform
                    if self.buildEndPlatform:
                        self.endPlatformWidth += charWidth
                        print(f"End Platform Width = {self.endPlatformWidth}")
                    else:
                        self.buildEndPlatform = True 
                elif char == 'X':  #enemy
                    newEnemy = Enemy(xCoods, currentCoods[1], self.enemyImages[0], self.enemyImages, 100)
                    self.enemies.append(newEnemy)
                    self.enemyGroup.append(newEnemy)
                    print(f"Enemy Added")
                elif char == '[': #building platform
                    self.buildPlatform = True
                    print(f"Starting platform build..")      
                elif char == ']': #end building platform
                    newPlatform = Platform(xCoods, currentCoods[1], self.platformImages[1])
                    self.platforms.append(newPlatform)
                    self.buildPlatform = False   
                    print(f"Platform Built and Added")  
        print("LOOP ENDED...build over...")           
                

    def reset(self):
        print("reset game...")
        self.player = Player(self.startingXPlayer, self.startingYPlayer, self.playerImages[1], self.playerImages)
        self.soundManager.stop_all_sound_effects()
        self.playerOnPlatform = False
        self.noMovement = False
        self.playerWin = False
        self.currentPlatform = None


        for enemy in self.enemyGroup:
            self.enemyGroup.append(enemy)
            self.objects.add(enemy)
            enemy.LoadImages(self.enemyImages)
          
    def runGame(self):
        print("Running game....")
        self.ticks = 1
       # print(f"Ticks....{self.ticks}")
        engineOn = True

        #backgrounds
        self.objects.add(self.background_0)
        for bg in self.backgroundManagerCloud.backgrounds:
            self.objects.add(bg)
        for bg in self.backgroundManagerHill.backgrounds:
            self.objects.add(bg)
        for bg in self.backgroundManagerMtn.backgrounds:
            self.objects.add(bg)

        print(f"Backgrounds added...")
        #platforms
        platform_group = pygame.sprite.Group()
        for platform in self.platforms:
            platform_group.add(platform)
            self.objects.add(platform)


        print(f"Platforms added...")
        #enemy       
        for enemy in self.enemyGroup:
            enemy.LoadImages(self.enemyImages)
            self.objects.add(enemy)
            

        print("Enemy added...")

        #fruit
        for fruit in self.fruits:
            self.objects.add(fruit)

        print("Fruits added...")

        #sound
        self.soundManager.load_sound_effect("Laser", self.soundEffects[0])
        self.soundManager.load_sound_effect("Jet", self.soundEffects[1])
        self.soundManager.load_sound_effect("Hit", self.soundEffects[2])
        self.soundManager.load_sound_effect("EnemyHit", self.soundEffects[3])
        self.soundManager.load_sound_effect("Theme", "assets\sounds\Theme.mp3")
        
        #player
        self.objects.add(self.player)
        self.splats = []
        last_time = 0
        self.movingTicks = 0

        self.soundManager.playTheme("Theme", 0)
        print("Engine starting...")

        while engineOn:
            self.ticks += 1
         #   print(f"ticks...{self.ticks}")
            # Calculate the time that has passed since the last frame
            current_time = pygame.time.get_ticks()
            delta_time = current_time - last_time
            last_time = current_time
            #print(f"Current Time: {current_time} Delta Time: {delta_time} Last Time: {current_time}")
            
            # Calculate the distance that the clouds/bg should move this frame
            cloud_distance = self.cloudSpeed * delta_time / 1000
            bg_distance = self.backgroundSpeed * delta_time / 1000
            bg_distance2 = self.backgroundSpeed * delta_time / 1000


            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE and self.playerOnPlatform  and self.player.falling == False:
                     #JUMPING
                    self.player.jumping = True
                    self.soundManager.play_sound_effect("Jet", 3)

            if not self.player.jumping:
                self.soundManager.stop_sound_effect("Jet")
           

            self.playerOnPlatform = False       
            self.playerWin = False
            #collision (on platform)        
            for platform in self.platforms:            
                if self.collisionDetect.check_collisionTop(self.player.rect, platform.collideRect):
                    self.playerOnPlatform = True
                    self.currentPlatform = platform          
                    if platform is self.endPlatform:
                        self.playerWin = True        
                    break
            
            self.noMovement = False

            if self.playerOnPlatform:
                self.player.Action(False, None, False, False)  #on platform
            else:
                self.player.Action(False,  None, True, False) #falling

            keys = pygame.key.get_pressed()

        #KEYS/ACTIONS     

            if self.player.rect.y <= 50:
                self.player.rect.y = 50
            #JUMPING 
            
            if self.player.jumping == True and self.lastDirection == Direction.RIGHT:
                    self.player.Action(True, Direction.RIGHT,  False, True)
                
            elif self.player.jumping == True and self.lastDirection == Direction.LEFT:
                    self.player.Action(True, Direction.LEFT, False, True)

            #MOVING RIGHT
            stuck = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                #enemies
                for fruit in self.fruits:
                    fruit.update(Direction.RIGHT, self.noMovement)

                self.player.Action(True, Direction.RIGHT)
                self.lastDirection = Direction.RIGHT
                self.backgroundManagerHill.update(Direction.RIGHT, self.noMovement, bg_distance)                   
                self.backgroundManagerMtn.update(Direction.RIGHT, self.noMovement, bg_distance2)  
                self.backgroundManagerCloud.update(Direction.RIGHT, self.noMovement, cloud_distance) 
                for platform in self.platforms:                           
                    platform.update(self.playerOnPlatform, self.player.rect, Direction.RIGHT, self.noMovement)              
           
           
            #MOVING LEFT
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                 #enemies           
                for fruit in self.fruits:
                    fruit.update(Direction.LEFT, self.noMovement)
            
                self.player.Action(True, Direction.LEFT)
                self.lastDirection = Direction.LEFT
                self.backgroundManagerHill.update(Direction.LEFT, self.noMovement, bg_distance)    
                self.backgroundManagerMtn.update(Direction.LEFT, self.noMovement, bg_distance2)    
                self.backgroundManagerCloud.update(Direction.LEFT, self.noMovement, cloud_distance) 
                for platform in self.platforms:                         
                    platform.update(self.playerOnPlatform, self.player.rect, Direction.LEFT, self.noMovement)                            
            #STILL
            else:
                #enemies
                if self.lastDirection == Direction.RIGHT:
                    self.player.Action(False, Direction.RIGHT)
                elif self.lastDirection == Direction.LEFT:
                    self.player.Action(False, Direction.LEFT)

        #shooting
            if self.player.shooting == False and (keys[pygame.K_p] or keys[pygame.K_q] ) and len(self.projectilesInAir) < 5:
                self.player.Action(False,Direction.RIGHT,False,False,True)
                self.soundManager.play_sound_effect("Laser", 1)

        #environment                               
        #set sprites
            #shooting
            if self.player.shooting:
                print("SHOOTING")
                newProjectile = Projectile(self.player.rect.x + 20, self.player.rect.y + 65, self.projectileImage)
                self.projectilesInAir.append(newProjectile)
                self.objects.add(newProjectile)
                if self.player.shootingTicks > 0 and self.player.shootingTicks < 80:
                    self.player.ActiveSprite(self.playerImages[6])
                elif self.player.shootingTicks > 80 and self.player.shootingTicks < 160:
                    self.player.ActiveSprite(self.playerImages[7])
                elif self.player.shootingTicks > 340 and self.player.shootingTicks < 420:
                    self.player.ActiveSprite(self.playerImages[8])           
            #jumping
            elif self.player.jumping and self.lastDirection == Direction.RIGHT:
                self.player.ActiveSprite(self.playerImageRightJumping)
            elif self.player.jumping and self.lastDirection == Direction.LEFT:
                self.player.ActiveSprite(self.playerImageLeftJumping)
            #still
            elif not self.player.moving and self.lastDirection == Direction.RIGHT:
                self.player.ActiveSprite(self.playerImageRightStill)
            elif not self.player.moving and self.lastDirection == Direction.LEFT:
                self.player.ActiveSprite(self.playerImageLeftStill)
            #moving
            elif self.player.moving and self.lastDirection == Direction.RIGHT:
                self.player.ActiveSprite(self.playerImageRightMoving)
            elif self.player.moving and self.lastDirection == Direction.LEFT:
                self.player.ActiveSprite(self.playerImageLeftMoving)
            
            
            
            if len(self.projectilesInAir) > 0:
                print("Projectiles in air")
                for projectile in self.projectilesInAir: 
                    print("PROJECTILE X: " + str(projectile.collideRect.x))                   
                    projectile.moving()
                    
                    if projectile.rect.x > self.screen_width:
                       # print("PROJECTILE LEFT SCREEN")
                        self.projectilesInAir.remove(projectile)
                        self.objects.remove(projectile)            
            
            #fruits
            for fruit in self.fruits:
                if not fruit.eaten:
                    if self.collisionDetect.check_collisionFruit(self.player.rect, fruit.collideRect):
                        fruit.collided = True
                        print("Player collided fruit")
                else:
                    if not fruit.addedScore:
                        self.player.AddToScore(fruit.score)
                        fruit.addedScore = True
                        self.objects.remove(fruit)
                
            #enemies              
            for enemy in self.enemies:   
                if not self.objects.__contains__(enemy):
                    enemy.reset()
                    self.objects.add(enemy)
                if not enemy.playSound:
                    enemy.playSound = True
                    self.soundManager.play_sound_effect("EnemyHit",2)   
                if enemy.dying:
                    enemy.Dying()
                    if not enemy.splatSet:
                        splat = Splat(enemy.rect.x, enemy.rect.y, self.effectImages[0])
                        self.objects.add(splat)
                        self.splats.append(splat)    
                        enemy.SetSplat(True)
             
                      
                    
                elif enemy.dead:
                    if self.enemies.__contains__(enemy):
                        self.enemies.remove(enemy)
                    if self.objects.__contains__(enemy):
                        self.objects.remove(enemy)
                else:    
                    speed = 2                
                    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        enemy.UpdateEnemyRight(speed)
                    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        enemy.UpdateEnemyLeft(speed)  
                    else:
                        enemy.UpdateEnemy(speed)  
                                            
                    if pygame.Rect.colliderect(enemy.rect, self.player.rect):
                        self.player.Hit()
                        self.soundManager.play_sound_effect("Hit", 4)

                    if len(self.projectilesInAir) > 0:
                        for projectile in self.projectilesInAir: 
                            if pygame.Rect.colliderect(enemy.rect, projectile.collideRect):
                                self.projectilesInAir.remove(projectile)
                                self.objects.remove(projectile)
                                enemy.Hit()
                                self.player.AddToScore(enemy.score)
                                enemy.playSound = False
          

            #death
            if self.player.rect.top > self.screen_height:
                self.player.InstaDie()
            
            if self.player.dying:
                self.player.Dying()
                if not self.player.splatSet:
                    splat = Splat(self.player.rect.x, self.player.rect.y, self.effectImages[0])
                    self.objects.add(splat)
                    self.splats.append(splat) 
                    self.player.splatSet = True


            for splat in self.splats:
                splat.move(splat.rect.x, splat.rect.y)
                splat.splatTicks += 1
                if splat.splatTicks < 50:
                    splat.ActiveSprite(self.effectImages[0])
                if splat.splatTicks > 50 and splat.splatTicks < 100:
                    splat.ActiveSprite(self.effectImages[1])
                if splat.splatTicks > 100 and splat.splatTicks < 200:
                    splat.ActiveSprite(self.effectImages[2])
                if splat.splatTicks > 200:                     
                    self.objects.remove(splat)
                    self.splats.remove(splat)

            
            if self.player.dead:
                self.soundManager.stop_all_sound_effects()
                engineOn = False
                #dead
                gameState = GameState.get_instance()
                gameState.state = State.DEATH
                gameState.set_score(self.player.score)

            #draw
            
            self.draw()

            if self.playerWin == True:
                engineOn = False
                #win
                gameState = GameState.get_instance()
                gameState.state = State.WIN

        self.soundManager.stop_all_sound_effects()
        print("Engine over.")

            
            

    def draw(self):
        # Clear the screen
        self.screen.fill("black")

        self.objects.draw(self.screen)

        self.player.draw(self.screen)

        # for platform in self.platforms:
        #     platform.draw_collision_rect(self.screen)

        for enemy in self.enemies:
            if enemy.dying:
                enemy.display_enemy_score(self.screen, enemy.score)

        for fruit in self.fruits:
            #fruit.draw_collision_rect(self.screen)
            if fruit.collided:
                fruit.display_fruity_score(self.screen)

        #level count
        # Create a text surface with the player's score
        level_text = self.font.render(f"Level: {self.currentLevel}", True, (255, 255, 255))  # You can change the color (here, white) as needed

        # Get the rectangle that represents the text surface
        level_rect = level_text.get_rect()
        level_rect.width = level_rect.width  * 2
        level_rect.height = level_rect.height * 1.5


        # Set the position of the text (top-left corner)
        level_rect.topleft = (self.screen_width - 150, 10)  # Adjust the position as needed

        
        # Create a translucent box behind the score
        level_box = pygame.Surface((level_rect.width, level_rect.height))
        level_box.set_alpha(200)  # Set the alpha value to control the transparency (0 is fully transparent, 255 is fully opaque)
        level_box.fill((128, 128, 128))  # Set the color of the box (gray in this case)
        self.screen.blit(level_box, level_rect.topleft)

        # Blit the text surface onto the screen
        self.screen.blit(level_text, (level_rect.x + level_rect.width /4, level_rect.y ))
        
        # Update the display
        pygame.display.update()



    
