import pygame
import random
from utils.button import Button
from game.settings import DEFAULT_FONT, SCREEN_WIDTH, SCREEN_HEIGHT
from core.enemy_stats import CombatEnemy

# now we get to the complicated stuff
# combat yay

# adding cards to the game
class Card:
    def __init__(self, name, cost, effect_type, value, element=None):
        self.name = name
        self.cost = cost
        self.effect_type = effect_type
        self.value = value
        self.element = element

    def play(self, player, enemy: CombatEnemy):
        if self.effect_type == "damage":
            dmg = random.randint(*self.value)
            # print(f"[DEBUG] Playing {self.name}, dealing {dmg} {self.element} damage")
            enemy.take_damage(dmg, damage_type=self.element)
            # print(f"[DEBUG] Enemy HP after play: {enemy.hp}")
        elif self.effect_type == "buff":
            setattr(player, self.value[0], self.value[1])
        elif self.effect_type == "debuff":
            setattr(enemy, self.value[0], self.value[1])
        elif self.effect_type == "heal":
            heal = random.randint(*self.value)
            player.hp = min(player.max_hp, player.hp + heal)
        elif self.effect_type == "special":
            if self.value == "gain_charge":
                player.charge += 3
            elif self.value == "redraw":
                player.discard.extend(player.hand)
                player.hand.clear()
                for _ in range(4):
                    player.draw_card()

# the player in combat, handling hp, damage types, charges, shuffling etc
class CombatPlayer:
    def __init__(self, deck):
        self.max_hp = 20
        self.hp = 20
        self.charge = 0
        self.deck = list(deck)
        random.shuffle(self.deck)
        self.hand = []
        self.discard = []
        self.unlocked_types = {1: "physical", 2: "void"}
        self.active_type = "physical"

        for _ in range(4):
            self.draw_card()

# drawing a card
    def draw_card(self):
        if not self.deck:
            self.deck, self.discard = self.discard, []
            random.shuffle(self.deck)
        if self.deck:
            self.hand.append(self.deck.pop())

# player taking damage
    def take_damage(self, amount):
        if getattr(self, "defensive_turns", 0) > 0:
            amount //= 2
            self.defensive_turns -= 1
        if getattr(self, "barrier_turns", 0) > 0:
            amount = 0
            self.barrier_turns -= 1
        self.hp = max(0, self.hp - amount)

# player speed calc
    def effective_speed(self):
        spd = getattr(self, "speed", 8)
        if getattr(self, "haste_turns", 0) > 0:
            spd *= 2
            self.haste_turns -= 1
        if getattr(self, "slow_turns", 0) > 0:
            spd //= 2
            self.slow_turns -= 1
        return max(1, spd)

# combat manager, handles turns
class CombatManager:
    def __init__(self, player: CombatPlayer, enemy: CombatEnemy):
        self.player = player
        self.enemy = enemy
        self.turn_meter = {"player": 0, "enemy": 0}
        self.turn_threshold = 100
        self.current_actor = None
        self.enemy_turn_active = False

# makes sure the player starts, so the combat doesnt break (guess how long it took me to figure out why i couldnt act in combat)
    def start_combat(self):
        self.current_actor = "player"
        self.enemy_turn_active = False
        self.turn_meter["player"] = 0
        self.turn_meter["enemy"] = 0
        # print("[DEBUG] Combat started, it's player's turn")

# and turns
    def advance_turns(self):
        if self.combat_over():
            return


        if not self.enemy_turn_active:
            self.turn_meter["player"] += self.player.effective_speed()
            self.turn_meter["enemy"] += self.enemy.effective_speed()

            if self.turn_meter["enemy"] >= self.turn_threshold:
                self.turn_meter["enemy"] -= self.turn_threshold
                self.current_actor = "enemy"
                self.enemy_turn_active = True
                # print("[DEBUG] Enemy turn started")

    def start_player_turn(self):
        self.current_actor = "player"
        self.enemy_turn_active = False

        self.player.charge += 1
        # print(f"[DEBUG] Player gains 1 charge → {self.player.charge}")

    def play_card(self, index, throw=False):
        if self.current_actor != "player":
            print("Not your turn")
            return

        if not (0 <= index < len(self.player.hand)):
            return

        card = self.player.hand[index]

        if throw:
            dmg = random.randint(2, 4)
            # print(f"[DEBUG] Throwing {card.name}, dealing {dmg} {self.player.active_type} damage")
            self.enemy.take_damage(dmg, damage_type=self.player.active_type)
        else:
            if self.player.charge >= card.cost:
                self.player.charge -= card.cost
                if card.effect_type == "damage":
                    dmg = random.randint(*card.value)
                    # print(f"[DEBUG] Playing {card.name}, dealing {dmg} {self.player.active_type} damage, {card.cost} charge consumed")
                    self.enemy.take_damage(dmg, damage_type=self.player.active_type)
                else:
                    card.play(self.player, self.enemy)
                # print(f"[DEBUG] Remaining charge: {self.player.charge}")
            else:
                # again drawing rather than printing but im too done with this for now
                print(f"Not enough charge to play {card.name}!")
                return

        self.player.discard.append(self.player.hand.pop(index))

        while len(self.player.hand) < 4:
            self.player.draw_card()

        if self.combat_over():
            return "win"

        self.current_actor = "enemy"
        self.enemy_turn_active = True

    def combat_over(self):
        return self.player.hp <= 0 or not self.enemy.is_alive()


# the screen, handles drawing, elements and the tutorial
class CombatScreen:
    tutorial_seen = False

    def __init__(self, screen, combat_manager):
        self.screen = screen
        self.combat = combat_manager
        self.card_buttons = []
        self.element_buttons = []
        self.hovered_card = None


        self.show_tutorial = not CombatScreen.tutorial_seen
        self.tutorial_ack = False

# elements
    def set_element(self, i):
        if i in self.combat.player.unlocked_types:
            self.combat.player.active_type = self.combat.player.unlocked_types[i]

# handle events check for finished combat, tutorial flag, buttons and co
    def handle_event(self, event):
        if self.combat.combat_over():
            return "combat_over"

        if self.show_tutorial and not self.tutorial_ack:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.tutorial_ack = True
                    CombatScreen.tutorial_seen = True
            return

        if self.combat.enemy_turn_active:
            #print("[DEBUG] Not player's turn, ignoring input")
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #print("[DEBUG] Escape pressed → flee")
            return "flee"

        self.hovered_card = None

        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            for btn in self.card_buttons + self.element_buttons:
                btn.handle_event(event)

                if btn.hovered and btn in self.card_buttons[:len(self.combat.player.hand) * 2]:
                    idx = self.card_buttons.index(btn) // 2
                    if idx < len(self.combat.player.hand):
                        self.hovered_card = self.combat.player.hand[idx]
                        #print(f"[DEBUG] Hovering over card: {self.hovered_card.name}")

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if btn.rect.collidepoint(event.pos) and btn.callback:
                        btn.callback()

    def update(self, dt):
        if self.combat.enemy_turn_active:
            dmg = self.combat.enemy.attack(self.combat.player)
            # print(f"[DEBUG] Enemy attacked for {dmg}, Player HP: {self.combat.player.hp}")
            self.combat.start_player_turn()


        if self.combat.combat_over():
            if self.combat.player.hp <= 0:
                return "lose"
            else:
                return "win"

# now to actually drawing the screen
    def draw(self):
        self.screen.fill((30, 30, 30))
        player = self.combat.player
        enemy = self.combat.enemy
        info_font = DEFAULT_FONT


        enemy_text = info_font.render(f"{enemy.name} HP: {enemy.hp} / {enemy.max_hp}", True, (255, 100, 100))
        self.screen.blit(enemy_text, (SCREEN_WIDTH // 2 - enemy_text.get_width() // 2, 20))


        player_text = info_font.render(f"Player HP: {player.hp} / {player.max_hp}  Charge: {player.charge}", True, (255, 255, 255))
        player_text_y = SCREEN_HEIGHT - 80
        self.screen.blit(player_text, (20, player_text_y))


        flee_hint = info_font.render("ESC: Flee", True, (200, 200, 200))
        self.screen.blit(flee_hint, (SCREEN_WIDTH - flee_hint.get_width() - 20, SCREEN_HEIGHT - 40))


        if self.show_tutorial and not self.tutorial_ack:
            overlay_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)
            pygame.draw.rect(self.screen, (20, 20, 20), overlay_rect)
            pygame.draw.rect(self.screen, (64, 224, 208), overlay_rect, 3)

# combat tutorial
            tutorial_lines = [
                "Combat Tutorial",
                "",
                "Click Card Name to PLAY Card",
                "Click THROW to deal small damage",
                "You gain 1 Charge per turn",
                "PLAY costs Charge - THROW is free",
                "Click Element Icons to change dmg type",
                "Watch enemy weaknesses and resistances",
                "",
                "Press 'i' to leave the Tutorial!"
            ]

            def wrap_text(text, font, max_width):
                words = text.split(" ")
                lines, current = [], ""
                for word in words:
                    test_line = f"{current} {word}".strip()
                    if font.size(test_line)[0] <= max_width:
                        current = test_line
                    else:
                        lines.append(current)
                        current = word
                if current:
                    lines.append(current)
                return lines

            y = overlay_rect.y + 20
            max_line_width = overlay_rect.width - 40
            for line in tutorial_lines:
                if line.strip() == "":
                    y += 30
                    continue
                for wrapped in wrap_text(line, info_font, max_line_width):
                    text_surf = info_font.render(wrapped, True, (255, 255, 255))
                    self.screen.blit(text_surf, (overlay_rect.x + 20, y))
                    y += 30
            return

# buttons
        self.card_buttons.clear()
        grid_rows, grid_cols = 2, 2
        card_vertical_spacing = 100
        card_horizontal_spacing = 40
        x_start = SCREEN_WIDTH // 2 - (grid_cols * (150 + card_horizontal_spacing)) // 2
        y_start = 100

        if getattr(self.combat, "enemy_turn_active", False):
            overlay_text = info_font.render("Enemy Turn!", True, (255, 0, 0))
            self.screen.blit(overlay_text, (SCREEN_WIDTH // 2 - overlay_text.get_width() // 2, 80))

        for idx, card in enumerate(player.hand[:4]):
            row = idx // grid_cols
            col = idx % grid_cols
            x = x_start + col * (150 + card_horizontal_spacing)
            y = y_start + row * (40 + card_vertical_spacing)


            text_surface = info_font.render(f"{card.name} ({card.cost})", True, (0, 0, 0))
            btn_width = max(150, text_surface.get_width() + 20)
            btn_height = 40


            def make_callback(index, throw=False):
                def callback():
                    action_type = "Throw" if throw else "Play"
                    card = self.combat.player.hand[index]
                    # print(f"[DEBUG] {action_type} action triggered on {card.name} (index {index})")
                    self.combat.play_card(index, throw)
                    # print(f"[DEBUG] After action → Enemy HP: {self.combat.enemy.hp}, Player HP: {self.combat.player.hp}")

                return callback


            play_btn = Button(
                f"{card.name} ({card.cost})",
                (x, y),
                callback=make_callback(idx, throw=False),
                width=btn_width,
                height=btn_height
            )
            play_btn.draw(self.screen)
            self.card_buttons.append(play_btn)


            throw_text_surface = info_font.render("Throw", True, (0, 0, 0))
            throw_width = max(btn_width, throw_text_surface.get_width() + 20)
            throw_btn = Button(
                "Throw",
                (x, y + btn_height + 5),
                callback=make_callback(idx, throw=True),
                width=throw_width,
                height=30
            )
            throw_btn.draw(self.screen)
            self.card_buttons.append(throw_btn)


        self.element_buttons.clear()
        y_bottom = player_text_y - 60
        button_size = 40
        spacing = 10
        total_width = 6 * button_size + 5 * spacing
        x_start = SCREEN_WIDTH // 2 - total_width // 2

        for i in range(1, 7):
            element = player.unlocked_types.get(i, None)


            icon = None
            if element:
                icon_path = f"assets/icons/{element}.png"
                try:
                    img = pygame.image.load(icon_path).convert_alpha()
                    icon = pygame.transform.smoothscale(img, (button_size, button_size))
                except FileNotFoundError:
                    pass


            x_pos = x_start + (i - 1) * (button_size + spacing)

            def make_callback(index=i):
                return lambda: self.set_element(index)


            btn = Button(
                text="?" if icon is None else "",
                pos=(x_pos, y_bottom),
                callback=make_callback(i),
                width=button_size,
                height=button_size
            )
            if icon:
                btn.image = icon

            btn.draw(self.screen)
            self.element_buttons.append(btn)


        if self.hovered_card:
            self.draw_tooltip(self.hovered_card)

# tips like weakness/resistance and co
    def draw_tooltip(self, card):
        lines = [f"{card.name} (Cost: {card.cost})"]


        if hasattr(card, "effect_type"):
            element = card.element if card.element else getattr(self.combat.player, "active_type", None)

            effect_line = f"Effect: {card.effect_type} {card.value}"
            if element:
                effect_line += f" ({element})"
            lines.append(effect_line)

            if card.effect_type == "damage" and element:
                if element in self.combat.enemy.weaknesses:
                    lines.append(f"Enemy is WEAK to {element}!")
                elif element in self.combat.enemy.resistances:
                    lines.append(f"Enemy RESISTS {element}!")


        tooltip_width = max(DEFAULT_FONT.size(line)[0] for line in lines) + 10
        tooltip_height = len(lines) * 20 + 10
        mx, my = pygame.mouse.get_pos()
        rect = pygame.Rect(mx, my - tooltip_height, tooltip_width, tooltip_height)

        pygame.draw.rect(self.screen, (50, 50, 50), rect)
        pygame.draw.rect(self.screen, (64, 224, 208), rect, 2)

        for i, line in enumerate(lines):
            text_surf = DEFAULT_FONT.render(line, True, (255, 255, 255))
            self.screen.blit(text_surf, (rect.x + 5, rect.y + 5 + i * 20))