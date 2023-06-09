import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sound_effects = {}

    def load_sound_effect(self, name, path):
        sound = pygame.mixer.Sound(path)
        self.sound_effects[name] = sound

    def playTheme(self, name, channel):
        sound = self.sound_effects.get(name)
        if sound:
             pygame.mixer.Channel(channel).play(sound, loops = -1)
             pygame.mixer.Channel(channel).set_volume(0.5)
        else:
            print(f"Sound effect '{name}' not found.")

    def play_sound_effect(self, name, channel):
        sound = self.sound_effects.get(name)
        if sound and not pygame.mixer.Channel(channel).get_busy():
            pygame.mixer.Channel(channel).play(sound)
     

    def stop_sound_effect(self, name):
        sound = self.sound_effects.get(name)
        if sound:
            sound.stop()
        else:
            print(f"Sound effect '{name}' not found.")

    def stop_all_sound_effects(self):
        pygame.mixer.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)