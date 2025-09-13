import pygame
from game.settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

# player class, also lacking sprite option as of today
class Player:
    def __init__(self, x, y, speed=100):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.speed = speed
        self.color = (64, 224, 208) # turquoise (can you guess my fav colour?)

# inputs
    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed * dt
        return dx, dy

# check collisions
    def update(self, dt, walls):
        dx, dy = self.handle_input(dt)

        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                elif dx < 0:
                    self.rect.left = wall.right

        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                elif dy < 0:
                    self.rect.top = wall.bottom

# clamping
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)



