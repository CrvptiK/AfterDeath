import pygame

TILE_SIZE = 64

class Room:
    def __init__(self, tilemap, npcs=None, enemies=None):
        self.tilemap = tilemap
        self.npcs = npcs if npcs else []
        self.enemies = enemies if enemies else []
        self.walls = self.generate_walls()

    def generate_walls(self):
        walls = []
        for row_index, row in enumerate(self.tilemap):
            for col_index, tile in enumerate(row):
                if tile == "#":
                    wall_rect = pygame.Rect(
                        col_index * TILE_SIZE,
                        row_index * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    walls.append(wall_rect)
        return walls