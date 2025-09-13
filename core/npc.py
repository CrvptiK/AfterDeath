import pygame

# NPC for overworld and tied into dialogue screen
class NPC:
    debug_show_interact = False

    def __init__(
        self,
        x, y,
        name,
        width=32, height=32,
        color=(0, 0, 255), # blueee
        dialogue=None,
        interact_margin=8
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

        self.portrait = None
        self.name = name
        self.dialogue = dialogue or [{"side": "left", "text": "Hello!", "portrait": None}]

        self.interact_margin = int(interact_margin)

    @property
    def interact_rect(self):

        m = self.interact_margin

        # bigger interact margin to enable overlap and thus interaction
        return self.rect.inflate(m * 2, m * 2)

    def interact(self, dialogue_screen):
        # print(f"[DEBUG] NPC {self.name} interacted!")
        dialogue_screen.start(self.dialogue)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

        if NPC.debug_show_interact:
            pygame.draw.rect(surface, (255, 255, 0), self.interact_rect, 1)
