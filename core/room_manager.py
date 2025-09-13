from core.overworld_enemy import OverworldEnemy
from core.room import Room
from core.item import Item
from core.npc import NPC

TILE_SIZE = 32

class RoomManager:
    def __init__(self):
        self.rooms = {}
        self.current_coords = (0, 0)
        self.load_rooms()

    def add_room(self, coords, tilemap, npcs=None, enemies=None, items=None, background_image=None):
        room = Room(tilemap, npcs, enemies, items)
        self.rooms[coords] = room

    def load_rooms(self):
# behold, my abominations of tilemaps (they are ugly as sin)
        # Room (0,0)
        tilemap_0 = [
            "####################",
            "#.##########.......#",
            "#..................#",
            "#..#####....#####..#",
            "#...........#####..#",
            "#..................#",
            "#..................#",
            "#...................",
            "#...................",
            "#..................#",
            "####...........#...#",
            "####..........###..#",
            "####...........#...#",
            "####...............#",
            "####################"
        ]
        room_0_npcs = [
            NPC(
                12 * TILE_SIZE, 9 * TILE_SIZE,
                name="Ghost",
                width=TILE_SIZE,
                height=TILE_SIZE,
                color=(0, 0, 255),
                dialogue=[{"side": "left","speaker": "Ghost", "text": "Wow! You look- rough! If I were you, I'd go back to bed..."}]
            )
        ]
        room_0_enemies = []
        room_0_items = [Item("Amulet", "Gives you the Void damage type.", 6 * TILE_SIZE, 8 * TILE_SIZE)]
        self.add_room((0, 0), tilemap_0, npcs=room_0_npcs, enemies=room_0_enemies,
                      items=room_0_items,
                      background_image="assets/maps/room0.png")

# in case you wish to play around with this: add or remove npcs, enemies or items, take note of the format, first int is x (horizontal), second is y (vertical) position
        # Room (1,0)
        tilemap_1 = [
            "####################",
            "#..................#",
            "#.....#####........#",
            "#..................#",
            "#..................#",
            "#...#######........#",
            "#............###...#",
            "....###.....####....",
            ".....####...####....",
            "#...........###...##",
            "#..........####..###",
            "#...........########",
            "#.....###..........#",
            "#...###............#",
            "####################"
        ]
        room_1_npcs = [
            NPC(
                15 * TILE_SIZE, 4 * TILE_SIZE,
                name="Ghost",
                width=TILE_SIZE,
                height=TILE_SIZE,
                color=(0, 0, 255),
                dialogue=[{"side": "left","speaker": "Ghost", "text": "Just follow the path East. Or don't. I don't care."}]
            )
        ]
        room_1_enemies = [OverworldEnemy(2 * TILE_SIZE, 3 * TILE_SIZE, enemy_type="zombie")]
        room_1_items = []
        self.add_room((1, 0), tilemap_1, room_1_npcs, room_1_enemies, room_1_items,)

        # Room (2,0)
        tilemap_2 = [
            "####################",
            "#..................#",
            "#.......######.....#",
            "#..................#",
            "#..###.............#",
            "#..................#",
            "#.......###........#",
            "......#######.......",
            ".....#########......",
            "#...###########....#",
            "#......####........#",
            "#.............###..#",
            "#..................#",
            "#..####............#",
            "####################"
        ]
        room_2_npcs = []
        room_2_enemies = [OverworldEnemy(4 * TILE_SIZE, 2 * TILE_SIZE, enemy_type="zombie"), OverworldEnemy(8 * TILE_SIZE, 12 * TILE_SIZE, enemy_type="skeleton")]
        room_2_items = [Item("Top Hat", "Makes ya look very dapper.", 15 * TILE_SIZE, 4 * TILE_SIZE)]
        self.add_room((2, 0), tilemap_2, room_2_npcs, room_2_enemies, room_2_items)

        # Room (3,0)
        tilemap_3 = [
            "####################",
            "#...##.............#",
            "#.#####............#",
            "#........##........#",
            "#......######......#",
            "#........##........#",
            "#........##....#####",
            "....##...##...##....",
            "....##...##...##....",
            "###########...##...#",
            "#..###........##...#",
            "#........###..##...#",
            "#....###########...#",
            "#..................#",
            "####################"
        ]
        room_3_npcs = []
        room_3_enemies = [OverworldEnemy(14 * TILE_SIZE, 2 * TILE_SIZE, enemy_type="zombie"), OverworldEnemy(5 * TILE_SIZE, 11 * TILE_SIZE, enemy_type="skeleton")]
        room_3_items = []
        self.add_room((3, 0), tilemap_3, room_3_npcs, room_3_enemies, room_3_items)

        # town map:
        # this is not populated
        # behold empty rooms ig

        # Room T1
        tilemap_t1 = [
            "####################",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#...................",
            "....................",
            "....................",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "####################"
        ]
        self.add_room((4, 0), tilemap_t1, npcs=[], enemies=[])

        # Room T2
        tilemap_t2 = [
            "####################",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "....................",
            "....................",
            "....................",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "########....########"
        ]
        self.add_room((5, 0), tilemap_t2, npcs=[], enemies=[])

        # Room T3
        tilemap_t3 = [
            "####################",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "...................#",
            "...................#",
            "...................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "####################"
        ]
        self.add_room((6, 0), tilemap_t3, npcs=[], enemies=[])

        # Room T4
        tilemap_t4 = [
            "####################",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#...................",
            "#...................",
            "#...................",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "########....########"
        ]
        self.add_room((4, 1), tilemap_t4, npcs=[], enemies=[])

        # Room T5
        tilemap_t5 = [
            "########....########",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "....................",
            "....................",
            "....................",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "########....########"
        ]
        self.add_room((5, 1), tilemap_t5, npcs=[], enemies=[])

        # Room T6
        tilemap_t6 = [
            "####################",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "...................#",
            "...................#",
            "...................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "####################"
        ]
        self.add_room((6, 1), tilemap_t6, npcs=[], enemies=[])

        # Room T7
        tilemap_t7 = [
            "########....########",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "####################"
        ]
        self.add_room((5, 2), tilemap_t7, npcs=[], enemies=[])

        # Room T8
        tilemap_t8 = [
            "########....########",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "####################"
        ]
        self.add_room((4, 2), tilemap_t8, npcs=[], enemies=[])

# player position and room transitions
    def get_current_room(self):
        return self.rooms.get(self.current_coords)

    def transition(self, direction):
        x, y = self.current_coords

        if direction == "right" and (x + 1, y) in self.rooms:
            self.current_coords = (x + 1, y)
        elif direction == "left" and (x - 1, y) in self.rooms:
            self.current_coords = (x - 1, y)
        elif direction == "down" and (x, y + 1) in self.rooms:
            self.current_coords = (x, y + 1)
        elif direction == "up" and (x, y - 1) in self.rooms:
            self.current_coords = (x, y - 1)
