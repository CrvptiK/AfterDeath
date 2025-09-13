import pygame
from utils.button import Button

# rip to you, if ya get this screen, jk jk
# the beautiful try again screen basically
class GameOverScreen:
    def __init__(self, font, screen_width, screen_height, background_path=None):
        self.font = font
        self.buttons = []

        center_x = screen_width // 2 - 100
        center_y = screen_height // 2

        self.buttons.append(
            Button("Return to Title", (center_x, center_y - 40), self.return_to_title, font=font)
        )
        self.buttons.append(
            Button("Quit", (center_x, center_y + 40), self.quit_game, font=font)
        )

        self.background = None
        if background_path:
            self.background = pygame.image.load(background_path).convert()

        self.fade_alpha = 255
        self.fade_speed = 5

        self.action = None

    def reset(self):
        self.fade_alpha = 255
        self.action = None

# buttons
    def return_to_title(self):
        self.action = "Return to Title"

    def quit_game(self):
        self.action = "Quit"

# handle button clicks
    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

        action = self.action
        self.action = None
        return action

# draw that screen
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