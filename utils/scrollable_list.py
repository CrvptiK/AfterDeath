import pygame

# importable scrollable list (used in keybinds screen for example)
class ScrollableList:
    def __init__(self, items, font, screen_width, screen_height, top_margin=100, line_spacing=10):
        self.items = items
        self.font = font
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.top_margin = top_margin
        self.line_spacing = line_spacing

        self.scroll_offset = 0
        self.line_height = self.font.get_linesize() + self.line_spacing

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.scroll_offset = max(self.scroll_offset - self.line_height, 0)
            elif event.button == 5:
                max_scroll = max(0, len(self.items) * self.line_height - (self.screen_height - self.top_margin))
                self.scroll_offset = min(self.scroll_offset + self.line_height, max_scroll)

    def draw(self, screen):
        y = self.top_margin - self.scroll_offset
        for text in self.items:
            surf = self.font.render(text, True, (200, 200, 200))
            rect = surf.get_rect(center=(self.screen_width // 2, y))
            screen.blit(surf, rect)
            y += self.line_height