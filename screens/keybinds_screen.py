import pygame
from utils.scrollable_list import ScrollableList

# for looking up controls in game ;)
class KeybindsScreen:
    def __init__(self, font, screen_width, screen_height):
        self.font = font
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.action = None

# everything i deemed important
        keybinds = [
            "Movement: Arrow Keys, WASD",
            "Interact: E",
            "Dialogue Skip/Confirm: Space",
            "Open Inventory: I",
            "Show Journal Info: J",
            "Pause: ESC",
            "Confirm: ENTER",
            "Cancel, Back: ESC"
        ]
        self.scrollable = ScrollableList(keybinds, font, screen_width, screen_height, top_margin=150)
# yes, you can scroll this (if it had more text)

    def handle_event(self, event):
        self.scrollable.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def draw(self, screen):
        title = self.font.render("Keybinds", True, (255, 255, 255))
        rect = title.get_rect(center=(self.screen_width // 2, 80))
        screen.blit(title, rect)

        self.scrollable.draw(screen)

