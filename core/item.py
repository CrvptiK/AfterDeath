import pygame
import os
from game.settings import TILE_SIZE

# item class for drawing and interacting with the item
class Item:
    def __init__(self, name, description="", x=0, y=0, image_folder="assets/items"):
        self.name = name
        self.description = description
        self.picked_up = False

        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

        image_path = os.path.join(image_folder, f"{name}.png")
        if os.path.exists(image_path):
            img = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        else:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((200, 200, 50))

    def draw(self, screen):
        if not self.picked_up:
            screen.blit(self.image, self.rect)

    def interact(self, player_inventory):
        if not self.picked_up:
            player_inventory.add_item(self)
            # flag to not draw item in overworld
            self.picked_up = True
            # Debug print(f"Picked up {self.name}")
            return True
        return False