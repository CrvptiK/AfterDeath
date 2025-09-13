import pygame
from utils.button import Button

class TitleScreen:
    def __init__(self, font, screen_width, screen_height, background_path=None):
        self.font = font
        self.buttons = []

        center_x = screen_width // 2 - 100

        self.buttons.append(
            Button("Start Game", (center_x, 200), self.start_game, font=font)
        )
        self.buttons.append(
            Button("Quit", (center_x, 300), self.quit_game, font=font)
        )

        self.action = None

        self.background = None
        if background_path:
            self.background = pygame.image.load(background_path).convert()

        self.fade_alpha = 255
        self.fade_speed = 5

    def reset(self):
        self.fade_alpha = 255
        self.action = None

# you can do a whole lot of two things here
    def start_game(self):
        self.action = "start"

    def quit_game(self):
        self.action = "quit"

# handling button click
    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

        action = self.action
        self.action = None
        return action

# drawing screen
    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        for button in self.buttons:
            button.draw(screen)

        if self.fade_alpha > 0:
            fade_surface = pygame.Surface(screen.get_size())
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(self.fade_alpha)
            screen.blit(fade_surface, (0, 0))
            self.fade_alpha = max(0, self.fade_alpha - self.fade_speed)