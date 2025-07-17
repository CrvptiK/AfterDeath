import pygame

class Player:
    def __init__(self, x, y):
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 3

    def handle_input(self, keys, obstacles):
        dx = dy = 0
        if keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_s]:
            dy = self.speed
        if keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_d]:
            dx = self.speed

        future_rect = self.rect.move(dx, 0)
        if not any(future_rect.colliderect(obj.rect if hasattr(obj, "rect") else obj) for obj in obstacles):
            self.rect.x += dx

        future_rect = self.rect.move(0, dy)
        if not any(future_rect.colliderect(obj.rect if hasattr(obj, "rect") else obj) for obj in obstacles):
            self.rect.y += dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)
