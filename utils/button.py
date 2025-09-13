import pygame
from game.settings import DEFAULT_FONT

# i got a whole bunch of- buttons
class Button:
    def __init__(self, text, pos, callback, width=200, height=50, font=None, image=None):
        self.text = text
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.callback = callback
        self.image = image
        self.hovered = False
        self.font = font or DEFAULT_FONT

    def draw(self, screen):
        bg_color = (64, 224, 208) if self.hovered else (80, 80, 80)
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=8)

        if hasattr(self, "image") and self.image:
            img_rect = self.image.get_rect(center=self.rect.center)
            screen.blit(self.image, img_rect)
        else:
            text_color = (0, 0, 0) if self.hovered else (255, 255, 255)
            text_surf = self.font.render(self.text, True, text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)


    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                self.callback()