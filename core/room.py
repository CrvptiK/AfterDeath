import os
import pygame

TILE_SIZE = 32

# room class, used in room manager
class Room:
    def __init__(self, tilemap, npcs=None, enemies=None, items=None, background_image=None):
        self.tilemap = tilemap
        self.npcs = npcs if npcs is not None else []
        self.enemies = enemies if enemies is not None else []
        self.items = items if items is not None else []
        self.walls = []
        self.doorways = {"left": [], "right": [], "up": [], "down": []}
        self._parse_tilemap()

        self.background = None
        if background_image and os.path.exists(background_image):
            self.background = pygame.image.load(background_image).convert()
            room_width = len(self.tilemap[0]) * TILE_SIZE
            room_height = len(self.tilemap) * TILE_SIZE
            self.background = pygame.transform.scale(self.background, (room_width, room_height))

# walls and doors
    def _parse_tilemap(self):
        rows = len(self.tilemap)
        cols = len(self.tilemap[0])

        for row_idx, row in enumerate(self.tilemap):
            for col_idx, char in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE

                if char == "#":
                    self.walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

        passage_size = TILE_SIZE * 3


        self._find_edge_gaps(self.tilemap[0], "horizontal", 0, passage_size)

        self._find_edge_gaps(self.tilemap[-1], "horizontal", (rows - 1) * TILE_SIZE, passage_size)

        col0 = "".join(row[0] for row in self.tilemap)
        self._find_edge_gaps(col0, "vertical", 0, passage_size)

        col_last = "".join(row[-1] for row in self.tilemap)
        self._find_edge_gaps(col_last, "vertical", (cols - 1) * TILE_SIZE, passage_size)

    def _find_edge_gaps(self, line, orientation, fixed_pos, min_size):
        start = None
        for i, ch in enumerate(line + "#"):
            if ch == "." and start is None:
                start = i
            elif ch != "." and start is not None:
                length = i - start
                if length >= min_size // TILE_SIZE:
                    if orientation == "horizontal":
                        rect = pygame.Rect(start * TILE_SIZE, fixed_pos, length * TILE_SIZE, TILE_SIZE)
                        if fixed_pos == 0:
                            self.doorways["up"].append(rect)
                        else:
                            self.doorways["down"].append(rect)
                    else:
                        rect = pygame.Rect(fixed_pos, start * TILE_SIZE, TILE_SIZE, length * TILE_SIZE)
                        if fixed_pos == 0:
                            self.doorways["left"].append(rect)
                        else:
                            self.doorways["right"].append(rect)
                start = None

# collision rects for collision logic
    def get_collision_rects(self, block_enemies=True):
        rects = list(self.walls)
        rects += [npc.rect for npc in self.npcs]
        if block_enemies:
            rects += [enemy.rect for enemy in self.enemies]
        return rects

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            for wall in self.walls:
                pygame.draw.rect(screen, (100, 100, 100), wall)

        for npc in self.npcs:
            npc.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        for item in self.items:
            item.draw(screen)