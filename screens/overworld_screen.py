import pygame

from core.npc import NPC
from core.room_manager import RoomManager
from core.player import Player
from screens.overworld_overlay import OverworldOverlay
from game.settings import DEFAULT_FONT, TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT


class OverworldScreen:
    def __init__(self, screen, clock, dialogue_screen, player_data):
        self.screen = screen
        self.clock = clock
        self.room_manager = RoomManager()
        self.player_data = player_data
        self.inventory = self.player_data.inventory
        self.transition_cooldown = 0
        self.dialogue_screen = dialogue_screen

        # Debug
        self.show_item_interact = False

        start_x, start_y = 5 * TILE_SIZE, 5 * TILE_SIZE
        self.player = Player(start_x, start_y)

        self.overlay = OverworldOverlay(DEFAULT_FONT, SCREEN_WIDTH)

# for the main state handler
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "pause"
            elif event.key == pygame.K_i:
                return "inventory"
            elif event.key == pygame.K_F1:
                NPC.debug_show_interact = not NPC.debug_show_interact
                self.show_item_interact = not self.show_item_interact
            elif event.key == pygame.K_e:
                return self.interact()
            elif event.key == pygame.K_j:
                self.overlay.toggle()
        return None

# collision and cooldowns
    def update(self, dt):
        if self.transition_cooldown > 0:
            self.transition_cooldown -= dt

        current_room = self.room_manager.get_current_room()

        collidables = []
        for obj in current_room.get_collision_rects():
            collidables.append(obj.rect if hasattr(obj, "rect") else obj)

        self.player.update(dt, collidables)

        for enemy in current_room.enemies:
            result = enemy.update(self.player)
            if result:
                enemy_type, combat_enemy, enemy_ref = result
                return ("combat", enemy_type, combat_enemy, enemy_ref)

        current_room.enemies = [e for e in current_room.enemies if not e.defeated]

        self.handle_room_transitions(current_room)

        return None

# room transition handler
    def handle_room_transitions(self, current_room):
        if self.transition_cooldown > 0:
            return

        room_width = SCREEN_WIDTH
        room_height = SCREEN_HEIGHT
        passage_size = TILE_SIZE * 3
        px, py = self.player.rect.center
        x, y = self.room_manager.current_coords


        if (x + 1, y) in self.room_manager.rooms:
            doorway_top = room_height / 2 - passage_size / 2
            doorway_bottom = room_height / 2 + passage_size / 2
            if self.player.rect.right >= room_width and doorway_top <= py <= doorway_bottom:
                self.room_manager.transition("right")
                self.player.rect.left = 1
                self.player.rect.centery = room_height / 2
                self.transition_cooldown = 0.2


        if (x - 1, y) in self.room_manager.rooms:
            doorway_top = room_height / 2 - passage_size / 2
            doorway_bottom = room_height / 2 + passage_size / 2
            if self.player.rect.left <= 0 and doorway_top <= py <= doorway_bottom:
                self.room_manager.transition("left")
                self.player.rect.right = room_width - 1
                self.player.rect.centery = room_height / 2
                self.transition_cooldown = 0.2


        if (x, y + 1) in self.room_manager.rooms:
            doorway_left = room_width / 2 - passage_size / 2
            doorway_right = room_width / 2 + passage_size / 2
            if self.player.rect.bottom >= room_height and doorway_left <= px <= doorway_right:
                self.room_manager.transition("down")
                self.player.rect.top = 1
                self.player.rect.centerx = room_width / 2
                self.transition_cooldown = 0.2


        if (x, y - 1) in self.room_manager.rooms:
            doorway_left = room_width / 2 - passage_size / 2
            doorway_right = room_width / 2 + passage_size / 2
            if self.player.rect.top <= 0 and doorway_left <= px <= doorway_right:
                self.room_manager.transition("up")
                self.player.rect.bottom = room_height - 1
                self.player.rect.centerx = room_width / 2
                self.transition_cooldown = 0.2

# check for interact
    def interact(self):
        # Debug
        # print("Interact called!")
        current_room = self.room_manager.get_current_room()

# state call dialogue
        for npc in current_room.npcs:
            if self.player.rect.colliderect(npc.interact_rect):
                npc.interact(self.dialogue_screen)
                return "dialogue"

# state call combat
        for enemy in current_room.enemies:
            if self.player.rect.colliderect(enemy.rect) and not enemy.defeated:
                enemy_type = enemy.interact(self.player)
                if enemy_type:
                    from core.enemy_stats import create_combat_enemy
                    combat_enemy = create_combat_enemy(enemy_type)
                    return ("combat", combat_enemy, enemy)


        current_room.enemies = [e for e in current_room.enemies if not e.defeated]

# pickup item call
        for item in current_room.items:
            if self.player.rect.colliderect(item.rect) and not item.picked_up:
                item.interact(self.inventory)
                # print(f"You picked up: {item.item.name}")

        # Debug
        # print("DEBUG: overworld inventory:", getattr(self, "inventory").list_items())
        # if hasattr(self, "player_data"):
            # print("DEBUG: player_data inventory:", self.player_data.inventory.list_items())

        current_room.items = [i for i in current_room.items if not i.picked_up]

        return None

# Debug, currently not needed but just incase
    """
    def debug_draw_rects(self):
        font = pygame.font.SysFont(None, 24)
        y_offset = 40  

        px, py, pw, ph = self.player.rect
        player_text = font.render(f"Player: ({px}, {py}, {pw}, {ph})", True, (0, 255, 0))
        self.screen.blit(player_text, (10, y_offset))
        y_offset += 20

        pygame.draw.rect(self.screen, (0, 255, 0), self.player.rect, 2)

        current_room = self.room_manager.get_current_room()
        for idx, npc in enumerate(current_room.npcs):
            nx, ny, nw, nh = npc.rect
            npc_text = font.render(
                f"NPC {idx} ({npc.name}): ({nx}, {ny}, {nw}, {nh})", True, (0, 0, 255)
            )
            self.screen.blit(npc_text, (10, y_offset))
            y_offset += 20

            if colliderect(self.player.rect, npc.rect):
                color = (255, 0, 0) 
            else:
                color = (0, 0, 255) 
            pygame.draw.rect(self.screen, color, npc.rect, 2)
    """

# visualsss
    def draw(self):
        current_room = self.room_manager.get_current_room()

        current_room.draw(self.screen)
        self.player.draw(self.screen)
        for npc in current_room.npcs:
            npc.draw(self.screen)
        for enemy in current_room.enemies:
            enemy.draw(self.screen)
        for item in current_room.items:
            item.draw(self.screen)

        self.overlay.draw(self.screen, self.player_data)

        if self.show_item_interact:
            for item in current_room.items:
                color = (255, 255, 0)
                pygame.draw.rect(self.screen, color, item.interact_rect, 2)

        # DEBUG
        # self.debug_draw_rects()

        # more DEBUG, enable to see town doors outlined, used while fixing transitions
        DEBUG_DOORS = False
        if DEBUG_DOORS:
            colors = {
                "up": (255, 0, 0),
                "down": (0, 255, 0),
                "left": (0, 0, 255),
                "right": (255, 255, 0)
            }
            room = self.room_manager.get_current_room()
            for side, doors in room.doorways.items():
                for door in doors:
                    pygame.draw.rect(self.screen, colors.get(side, (255, 255, 255)), door, 2)
