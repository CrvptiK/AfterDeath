import pygame
from utils.button import Button


# le pause screen, just a bunch of buttons basically
class PauseScreen:
    def __init__(self, font, screen_width, screen_height):
        self.font = font
        self.buttons = []

        center_x = screen_width // 2 - 100
        center_y = screen_height // 2

        self.buttons.append(
            Button("Resume", (center_x, center_y - 90), self.resume, font=font)
        )
        self.buttons.append(
            Button("Keybinds", (center_x, center_y - 30), self.show_keybinds, font=font)
        )
        self.buttons.append(
            Button("Quit to Title", (center_x, center_y + 30), self.quit_to_title, font=font)
        )
        self.buttons.append(
            Button("Exit Game", (center_x, center_y + 90), self.exit_game, font=font)
        )

        self.action = None

    def resume(self):
        self.action = "Resume"

    def show_keybinds(self):
        self.action = "Keybinds"

    def quit_to_title(self):
        self.action = "Quit to Title"

    def exit_game(self):
        self.action = "Exit Game"

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)
        action = self.action
        self.action = None
        return action

    def draw(self, screen):
        pause_surf = self.font.render("Paused", True, (255, 255, 255))
        pause_rect = pause_surf.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(pause_surf, pause_rect)

        for button in self.buttons:
            button.draw(screen)
