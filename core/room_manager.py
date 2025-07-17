from core.npc import NPC
from core.enemy import Enemy
from core.room import Room

TILE_SIZE = 64

class RoomManager:
    def __init__(self):
        self.rooms = {}
        self.current_coords = (0, 0)
        self.load_rooms()

    def load_rooms(self):
        tilemap_0 = [
            "################",
            "#..............#",
            "#..##..........#",
            "#..............#",
            "#......####....#",
            "#..............#",
            "################"
        ]
        room_0_npcs = [NPC(3 * TILE_SIZE, 1 * TILE_SIZE, "Hello there!")]
        room_0_enemies = []
        self.rooms[(0, 0)] = Room(tilemap_0, room_0_npcs, room_0_enemies)

        tilemap_1 = [
            "################",
            "...............#",
            ".....#####.....#",
            "...............#",
            "...####........#",
            "...............#",
            "################"
        ]
        room_1_npcs = [NPC(2 * TILE_SIZE, 1 * TILE_SIZE, "Need help?")]
        room_1_enemies = [Enemy(1 * TILE_SIZE, 2 * TILE_SIZE)]
        self.rooms[(1, 0)] = Room(tilemap_1, room_1_npcs, room_1_enemies)

    def get_current_room(self):
        return self.rooms.get(self.current_coords)

    def transition(self, direction):
        x, y = self.current_coords
        if direction == "right":
            self.current_coords = (x + 1, y)
        elif direction == "left":
            self.current_coords = (x - 1, y)
        elif direction == "up":
            self.current_coords = (x, y - 1)
        elif direction == "down":
            self.current_coords = (x, y + 1)