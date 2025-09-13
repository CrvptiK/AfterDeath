import pygame

# music player, thank pygame for its many built-in features
class MusicManager:
    def __init__(self):
        self.current_track = None

    def play(self, filepath, loop=True, fadeout_ms=1000):
        if self.current_track == filepath:
            return

        pygame.mixer.music.fadeout(fadeout_ms)

        pygame.mixer.music.load(filepath)
        if loop:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.play(0)

        self.current_track = filepath

    def stop(self):
        pygame.mixer.music.stop()
        self.current_track = None