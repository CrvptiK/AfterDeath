import pygame

class OverworldOverlay:

# some extra info for the player when they demand it, no missions do not automatically update yet
    def __init__(self, font, screen_width):
        self.font = font
        self.screen_width = screen_width
        self.visible = False
        self.mission_text = "Make your way to Limstedt!"

    def toggle(self):
        self.visible = not self.visible

    def draw(self, screen, player_data):
        if not self.visible:
            return

        hp_text = f"HP: {player_data.hp}/{player_data.max_hp}"
        hp_surf = self.font.render(hp_text, True, (255, 255, 255))
        hp_rect = hp_surf.get_rect(topleft=(10, 10))
        pygame.draw.rect(screen, (0, 0, 0), hp_rect.inflate(20, 10))
        screen.blit(hp_surf, hp_rect)

        mission_surf = self.font.render(self.mission_text, True, (64, 224, 208))
        mission_rect = mission_surf.get_rect(topright=(self.screen_width - 10, 10))
        pygame.draw.rect(screen, (0, 0, 0), mission_rect.inflate(20, 10))
        screen.blit(mission_surf, mission_rect)
