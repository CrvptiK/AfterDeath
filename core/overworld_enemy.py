import pygame
from core.enemy_stats import create_combat_enemy

class OverworldEnemy:
    debug_show_interact = False

# enemy rect colours
    COLOR_MAP = {
        "zombie": (100, 0, 0),
        "skeleton": (120, 10, 10),
        "time keeper": (80, 20, 10),
    }

# decided not to add alternate drawing option (sprite instead of rect) im lazy ok
    def __init__(self, x, y, enemy_type="zombie", interact_margin=2):
        self.enemy_type = enemy_type
        self.image = pygame.Surface((32, 32))
        self.image.fill(OverworldEnemy.COLOR_MAP.get(enemy_type, (255, 0, 0)))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.interact_margin = int(interact_margin)
        self.defeated = False
        self.combat_cooldown = 0
        self.cooldown_duration = 240

    # small margin to ensure overlap and thus collision detection
    @property
    def trigger_rect(self):
        m = self.interact_margin
        return self.rect.inflate(m * 1.2, m * 1.2)

# make sure that fleeing is possible via cooldown
    def update(self, player):
        if self.combat_cooldown > 0:
            self.combat_cooldown -= 1

        if not self.defeated and self.combat_cooldown == 0 and player.rect.colliderect(self.trigger_rect):
            # Debug print(f"Combat started with {self.enemy_type}!")
            combat_enemy = create_combat_enemy(self.enemy_type)

            self.combat_cooldown = self.cooldown_duration
            return self.enemy_type, combat_enemy, self

        return None

    def draw(self, surface):
        if not self.defeated:
            surface.blit(self.image, self.rect)
            if OverworldEnemy.debug_show_interact:
                pygame.draw.rect(surface, (255, 0, 0), self.trigger_rect, 1)
