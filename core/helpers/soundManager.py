import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sound_effects = {}

    def load_sound_effect(self, name, path):
        sound = pygame.mixer.Sound(path)
        self.sound_effects[name] = sound

    def play_sound_effect(self, name):
        sound = self.sound_effects.get(name)
        if sound:
            sound.play()
        else:
            print(f"Sound effect '{name}' not found.")

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