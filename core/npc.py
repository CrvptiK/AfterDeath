import pygame

class NPC:
    def __init__(self, x, y, message=None):
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.message = message
        self.interacted = False

    def interact(self):
        if self.message:
            print(f"{self.message}")
            self.interacted = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)
