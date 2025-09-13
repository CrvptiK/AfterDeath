import pygame
from game.settings import DEFAULT_FONT, SCREEN_WIDTH, SCREEN_HEIGHT

# this consists of two parts, basically, inventory and deck builder
# inventory
class InventoryScreen:
    def __init__(self, player_data):
        self.player_data = player_data
        self.tab = "items"

        self.working_deck = list(player_data.deck)

        self.hovered_item = None
        self.selected_item = None

        self.selected_index = 0
        self.hovered_card = None
        self.error_message = None

        self.save_button_rect = pygame.Rect(400, 450, 160, 40)
        self.save_button_rect = pygame.Rect(400, 450, 160, 40)
        self.cancel_button_rect = pygame.Rect(580, 450, 160, 40)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_i):
                if self.tab == "deck" and self.working_deck != self.player_data.deck:
                    self.error_message = "Confirm deck before exiting!"
                    return None
                return "close"

# handle inventory tab switch
            if event.key == pygame.K_TAB:
                self.tab = "deck" if self.tab == "items" else "items"
                self.selected_index = 0
                self.error_message = None

            if self.tab == "deck" and event.key == pygame.K_RETURN:
                if self.confirm_deck():
                    return "close"

# look at items
        if self.tab == "items":
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                self.update_hovered_item(mx, my)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                y_offset = 60
                for item in self.player_data.inventory.list_items():
                    rect = pygame.Rect(40, y_offset, 200, 24)
                    if rect.collidepoint(mx, my):
                        self.selected_item = item
                        break
                    y_offset += 30

# buttons
        if self.tab == "deck":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()

                if self.save_button_rect.collidepoint(mx, my):
                    self.confirm_deck()
                    return None

                if self.cancel_button_rect.collidepoint(mx, my):
                    self.working_deck = list(self.player_data.deck)
                    self.error_message = "Changes discarded"
                    return None

                self.handle_click(mx, my)

        return None

# check and warn if deck isnt suitable
    def add_to_deck(self, card):
        if len(self.working_deck) >= 20:
            self.error_message = "Deck cannot exceed 20 cards!"
            return

        count = sum(1 for c in self.working_deck if c.name == card.name)
        if count >= 2:
            self.error_message = f"Maxed copies of {card.name}!"
            return

        self.working_deck.append(card)
        self.error_message = None

    def remove_from_deck(self, card):
        if len(self.working_deck) <= 10:
            self.error_message = "Deck must have at least 10 cards!"
            return

        for i, c in enumerate(self.working_deck):
            if c.name == card.name:
                del self.working_deck[i]
                self.error_message = None
                return

        self.error_message = f"{card.name} not in deck!"

# double check when leaving card screen
    def confirm_deck(self):
        if len(self.working_deck) < 10:
            self.error_message = "Deck must have at least 10 cards!"
            return False
        if len(self.working_deck) > 20:
            self.error_message = "Deck cannot exceed 20 cards!"
            return False

        self.player_data.deck = list(self.working_deck)
        self.error_message = "Deck saved!"
        return True

    def update_hovered_item(self, mx, my):
        self.hovered_item = None
        y_offset = 60
        for item in self.player_data.inventory.list_items():
            rect = pygame.Rect(40, y_offset, 200, 24)
            if rect.collidepoint(mx, my):
                self.hovered_item = item
                break
            y_offset += 30

# what the tin says
    def show_item_info(self, item):

        print(f"Item Info: {item.name} - {item.description}")

    def handle_click(self, mx, my):

        y_offset = 60
        for card in self.player_data.card_library:
            rect = pygame.Rect(40, y_offset, 200, 24)
            if rect.collidepoint(mx, my):
                self.add_to_deck(card)
                return
            y_offset += 30

        y_offset = 60
        counts = self.get_deck_counts()
        for card, count in counts.items():
            rect = pygame.Rect(400, y_offset, 200, 24)
            if rect.collidepoint(mx, my):
                self.remove_from_deck(card)
                return
            y_offset += 30

# draw screen with tab info
    def draw(self, screen):
        screen.fill((20, 20, 20))

        title_surface = DEFAULT_FONT.render(f"Inventory - {self.tab.upper()}", True, (255, 255, 255))
        screen.blit(title_surface, (20, 20))

        instruction_text = "TAB switch to Deck Builder" if self.tab == "items" else "TAB switch to Inventory"
        instr_surface = DEFAULT_FONT.render(instruction_text, True, (0, 128, 128))
        screen.blit(instr_surface, (SCREEN_WIDTH - instr_surface.get_width() - 20, 20))

# handle states basically
        if self.tab == "items":
            self.draw_items(screen)
        elif self.tab == "deck":
            self.draw_deck(screen)

# drawing the items
    def draw_items(self, screen):
        y_offset = 60
        for obj in self.player_data.inventory.list_items():
            item = obj.item if hasattr(obj, "item") else obj

            text_surface = DEFAULT_FONT.render(item.name, True, (64, 224, 208))

            if hasattr(item, "image") and item.image:
                text_height = text_surface.get_height()
                img = pygame.transform.scale(item.image, (text_height, text_height))
                screen.blit(img, (40, y_offset))

                screen.blit(text_surface, (40 + text_height + 5, y_offset))
            else:
                screen.blit(text_surface, (40, y_offset))

            y_offset += 30

        panel_height = 120
        panel_rect = pygame.Rect(0, SCREEN_HEIGHT - panel_height, SCREEN_WIDTH, panel_height)
        pygame.draw.rect(screen, (0, 128, 128), panel_rect)
        pygame.draw.rect(screen, (255, 255, 255), panel_rect, 2)

        if self.selected_item:
            sel_item = self.selected_item.item if hasattr(self.selected_item, "item") else self.selected_item
            lines = [sel_item.name]
            if sel_item.description:
                words = sel_item.description.split()
                line = ""
                wrapped_lines = []
                for word in words:
                    test_line = f"{line} {word}".strip()
                    if DEFAULT_FONT.size(test_line)[0] > SCREEN_WIDTH - 20:
                        wrapped_lines.append(line)
                        line = word
                    else:
                        line = test_line
                wrapped_lines.append(line)
                lines.extend(wrapped_lines)

            for i, line in enumerate(lines):
                text = DEFAULT_FONT.render(line, True, (255, 255, 255))
                screen.blit(text, (10, SCREEN_HEIGHT - panel_height + 10 + i * 20))

        #Debug
        #print("Inventory items:", self.player_data.inventory.list_items())

# check and draw card number in deck
    def get_deck_counts(self):
        counts = {}
        for card in self.working_deck:
            counts[card.name] = counts.get(card.name, 0) + 1
        return counts

# draw le deck
    def draw_deck(self, screen):
        mx, my = pygame.mouse.get_pos()
        self.hovered_card = None


        y_offset = 60
        for card in self.player_data.card_library:
            rect = pygame.Rect(40, y_offset, 200, 24)
            color = (255, 255, 0) if rect.collidepoint(mx, my) else (200, 200, 200)

            name = card.name
            while DEFAULT_FONT.size(name)[0] > rect.width - 10 and len(name) > 3:
                name = name[:-1]

            text_surface = DEFAULT_FONT.render(name, True, color)
            screen.blit(text_surface, rect.topleft)
            if rect.collidepoint(mx, my):
                self.hovered_card = card
            y_offset += 30


        y_offset = 60
        counts = self.get_deck_counts()
        for card_name, count in counts.items():
            rect = pygame.Rect(SCREEN_WIDTH - 280, y_offset, 240, 24)
            display_text = f"{card_name} x{count}"

            while DEFAULT_FONT.size(display_text)[0] > rect.width - 10 and len(display_text) > 3:
                display_text = display_text[:-2] + "…"

            text_surface = DEFAULT_FONT.render(display_text, True, (64, 224, 208))
            screen.blit(text_surface, rect.topleft)
            if rect.collidepoint(mx, my):
                for c in self.working_deck:
                    if c.name == card_name:
                        self.hovered_card = c
                        break
            y_offset += 30

        deck_size_text = DEFAULT_FONT.render(f"Deck size: {len(self.working_deck)}/20", True, (255, 255, 255))
        screen.blit(deck_size_text, (400, SCREEN_HEIGHT - 120))

# buttons to save and discard, with wrap and hover effect
        def draw_button(rect, text, hover, base_color, hover_color):
            color = hover_color if hover else base_color
            pygame.draw.rect(screen, color, rect, border_radius=6)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=6)
            text_surface = DEFAULT_FONT.render(text, True, (0, 0, 0))
            screen.blit(text_surface, text_surface.get_rect(center=rect.center))

        save_text = "Save Deck"
        discard_text = "Discard Changes"

        save_width = DEFAULT_FONT.size(save_text)[0] + 20
        discard_width = DEFAULT_FONT.size(discard_text)[0] + 20
        button_height = 40

        total_width = save_width + 20 + discard_width
        start_x = (SCREEN_WIDTH - total_width) // 2
        y_pos = SCREEN_HEIGHT - 80

        self.save_button_rect = pygame.Rect(start_x, y_pos, save_width, button_height)
        self.cancel_button_rect = pygame.Rect(start_x + save_width + 20, y_pos, discard_width, button_height)

        hover_save = self.save_button_rect.collidepoint(mx, my)
        draw_button(
            self.save_button_rect, save_text, hover_save,
            base_color=(64, 224, 208),
            hover_color=(128, 255, 240)
        )

        hover_cancel = self.cancel_button_rect.collidepoint(mx, my)
        draw_button(
            self.cancel_button_rect, discard_text, hover_cancel,
            base_color=(0, 128, 128),
            hover_color=(32, 178, 170)
        )

        if self.hovered_card:
            self.draw_tooltip(screen, self.hovered_card, mx, my)

        if self.error_message:
            error_surface = DEFAULT_FONT.render(self.error_message, True, (255, 50, 50))
            screen.blit(error_surface, (40, SCREEN_HEIGHT - 120))

# and a bit of info on the cards, while hovering them
    def draw_tooltip(self, screen, card, x, y):
        lines = [card.name]
        if hasattr(card, "type"):
            lines.append(f"Type: {card.type}")
        if hasattr(card, "cost"):
            lines.append(f"Cost: {card.cost}")
        if hasattr(card, "effect"):
            lines.append(f"Effect: {card.effect}")

        tooltip_width = max(DEFAULT_FONT.size(line)[0] for line in lines) + 10
        tooltip_height = len(lines) * 20 + 10
        rect = pygame.Rect(x, y, tooltip_width, tooltip_height)

        pygame.draw.rect(screen, (50, 50, 50), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)

        for i, line in enumerate(lines):
            text = DEFAULT_FONT.render(line, True, (255, 255, 255))
            screen.blit(text, (x + 5, y + 5 + i * 20))
