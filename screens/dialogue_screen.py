import pygame
import os


# drawing the screen for npc interaction
class DialogueScreen:
    def __init__(self, font, screen_width, screen_height,
                 portrait_folder="assets/portraits", bg_image_path=None):
        self.font = font
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.portrait_folder = portrait_folder

        self.background = None
        if bg_image_path and os.path.exists(bg_image_path):
            self.background = pygame.image.load(bg_image_path).convert()
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

        self.active = False
        self.dialogue_lines = []
        self.current_line = 0

        self.char_index = 0
        self.revealed_text = ""
        self.text_speed = 50
        self.fast_speed = 15
        self.last_update = 0

        self.portraits = {}

        self.portrait_size = (480, 480)

    def start(self, lines):
        self.dialogue_lines = lines
        self.current_line = 0
        self.char_index = 0
        self.revealed_text = ""
        self.last_update = pygame.time.get_ticks()
        self.active = True

# detect inputs to skip or leave
    def handle_event(self, event):
        if not self.active:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                line_text = self.dialogue_lines[self.current_line]["text"]
                if self.char_index < len(line_text):
                    self.char_index = len(line_text)
                    self.revealed_text = line_text
                else:
                    self.current_line += 1
                    if self.current_line >= len(self.dialogue_lines):
                        self.active = False
                        return "end"
                    self.char_index = 0
                    self.revealed_text = ""
                    self.last_update = pygame.time.get_ticks()
            elif event.key == pygame.K_ESCAPE:
                self.active = False
                return "end"

        return None

    def update(self):
        if not self.active:
            return

        line = self.dialogue_lines[self.current_line]["text"]
        now = pygame.time.get_ticks()
        speed = self.fast_speed if pygame.key.get_mods() & pygame.KMOD_SHIFT else self.text_speed

        if self.char_index < len(line):
            if now - self.last_update > speed:
                self.char_index += 1
                self.revealed_text = line[:self.char_index]
                self.last_update = now

# make sure text is in the box and doesnt run off-screen
    def wrap_text(self, text, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            test_surf = self.font.render(test_line, True, (255, 255, 255))
            if test_surf.get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines

# draw the speaker
    def get_portrait(self, speaker):
        if speaker in self.portraits:
            return self.portraits[speaker]

        portrait_path = os.path.join(self.portrait_folder, f"{speaker}.png")
        if os.path.exists(portrait_path):
            portrait = pygame.image.load(portrait_path).convert_alpha()
            portrait = pygame.transform.smoothscale(portrait, self.portrait_size)
            self.portraits[speaker] = portrait
            return portrait
        return None

    def draw(self, screen):
        if not self.active:
            return

        line_data = self.dialogue_lines[self.current_line]
        side = line_data.get("side", "left")
        speaker = line_data.get("speaker", None)

        if self.background:
            screen.blit(self.background, (0, 0))

        portrait = self.get_portrait(speaker) if speaker else None
        if portrait:
            portrait_x = - 40 if side == "left" else self.screen_width - 60 - self.portrait_size[0]
            portrait_y = self.screen_height - 400
            screen.blit(portrait, (portrait_x, portrait_y))
        else:
            placeholder_rect = pygame.Rect(60, self.screen_height - 250, *self.portrait_size)
            pygame.draw.rect(screen, (200, 200, 200), placeholder_rect)
            pygame.draw.rect(screen, (255, 255, 255), placeholder_rect, 2)

        box_rect = pygame.Rect(50, self.screen_height - 150, self.screen_width - 100, 120)
        pygame.draw.rect(screen, (0, 0, 0), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)

        if speaker:
            name_surface = self.font.render(speaker, True, (64, 224, 208))
            name_bg = pygame.Rect(box_rect.x + 10, box_rect.y - 25, name_surface.get_width() + 10, 25)
            pygame.draw.rect(screen, (0, 0, 0), name_bg)
            pygame.draw.rect(screen, (255, 255, 255), name_bg, 2)
            screen.blit(name_surface, (name_bg.x + 5, name_bg.y + 1))

        max_text_width = box_rect.width - 40
        wrapped_lines = self.wrap_text(self.revealed_text, max_text_width)
        y_offset = self.screen_height - 130
        for line in wrapped_lines:
            text_surf = self.font.render(line, True, (255, 255, 255))
            screen.blit(text_surf, (70, y_offset))
            y_offset += self.font.get_linesize()

