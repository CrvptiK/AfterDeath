import pygame
import sys

from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game.settings import FONT_PATH, DEFAULT_FONT_SIZE

from screens.title_screen import TitleScreen
from screens.pause_screen import PauseScreen
from screens.overworld_screen import OverworldScreen
from screens.inventory_screen import InventoryScreen
from screens.keybinds_screen import KeybindsScreen
from screens.dialogue_screen import DialogueScreen
from screens.game_over_screen import GameOverScreen
from utils.music_manager import MusicManager


def main(player_data):
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AfterLife")
    clock = pygame.time.Clock()

    pygame.font.init()
    font = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE)

    state = "title"

    title_screen = TitleScreen(
        font, SCREEN_WIDTH, SCREEN_HEIGHT, background_path="assets/images/title.png"
    )
    title_screen.reset()
    game_over_screen = GameOverScreen(
        font,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        background_path="assets/images/game_over.png"
    )
    pause_screen = PauseScreen(font, SCREEN_WIDTH, SCREEN_HEIGHT)
    keybinds_screen = KeybindsScreen(font, SCREEN_WIDTH, SCREEN_HEIGHT)
    dialogue_screen = DialogueScreen(font, SCREEN_WIDTH, SCREEN_HEIGHT, bg_image_path="assets/images/dialogue_bg.png")
    overworld_screen = OverworldScreen(screen, clock, dialogue_screen, player_data)
    inventory_screen = InventoryScreen(player_data)

    combat_screen = None
    overworld_enemy_ref = None

    music = MusicManager()

    SONGS = {
        "title": "assets/music/lacrimosa.mp3",
        "overworld": "assets/music/danse_macabre.mp3",
        "combat": "assets/music/seasons.mp3",
        "gameover": "assets/music/suspicion.mp3",
    }

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "title":
                music.play(SONGS["title"], loop=True)
                action = title_screen.handle_event(event)
                if action == "start":
                    state = "overworld"
                elif action == "quit":
                    running = False

            elif state == "overworld":
                music.play(SONGS["overworld"], loop=True)
                action = overworld_screen.handle_event(event)
                if action == "pause":
                    state = "pause"
                elif action == "inventory":
                    state = "inventory"
                elif action == "dialogue":
                    state = "dialogue"

            elif state == "inventory":
                action = inventory_screen.handle_event(event)
                if action == "close":
                    state = "overworld"

            elif state == "pause":
                action = pause_screen.handle_event(event)
                if action == "Resume":
                    state = "overworld"
                elif action == "Keybinds":
                    state = "keybinds"
                elif action == "Quit to Title":
                    state = "title"
                    title_screen.reset()
                    title_screen.action = None
                elif action == "Exit Game":
                    running = False

            elif state == "keybinds":
                action = keybinds_screen.handle_event(event)
                if action == "back":
                    state = "pause"

            elif state == "dialogue":
                action = dialogue_screen.handle_event(event)
                if action == "end":
                    state = "overworld"


            elif state == "combat":
                music.play(SONGS["combat"], loop=True)
                action = combat_screen.handle_event(event)
                if action == "flee":
                    state = "overworld"
                    combat_screen = None
                    continue

                result = combat_screen.update(dt)
                if result == "win":
                    if overworld_enemy_ref:
                        overworld_enemy_ref.defeated = True
                    state = "overworld"
                    combat_screen = None
                elif result == "lose":
                    state = "game_over"
                    combat_screen = None
                    game_over_screen.reset()

            elif state == "game_over":
                music.play(SONGS["gameover"], loop=False)
                action = game_over_screen.handle_event(event)
                if action == "Return to Title":
                    state = "title"
                elif action == "Quit":
                    running = False

        if state == "overworld":
            action = overworld_screen.update(dt)

            if isinstance(action, tuple) and action[0] == "combat":
                _, enemy_type, combat_enemy, enemy_ref = action

                from screens.combat_screen import CombatPlayer, CombatManager, CombatScreen
                combat_player = CombatPlayer(player_data.deck)
                combat_manager = CombatManager(combat_player, combat_enemy)
                combat_manager.start_combat()
                combat_screen = CombatScreen(screen, combat_manager)

                overworld_enemy_ref = enemy_ref
                state = "combat"

        if state == "combat" and combat_screen:
            if hasattr(combat_screen, "update"):
                combat_screen.update(dt)

        screen.fill((20, 20, 20))

        if state == "title":
            title_screen.draw(screen)
        elif state == "overworld":
            overworld_screen.draw()
        elif state == "inventory":
            inventory_screen.draw(screen)
        elif state == "pause":
            overworld_screen.draw()
            pause_screen.draw(screen)
        elif state == "keybinds":
            keybinds_screen.draw(screen)
        elif state == "dialogue":
            dialogue_screen.update()
            dialogue_screen.draw(screen)
        elif state == "combat" and combat_screen:
            combat_screen.draw()
            combat_screen.update(dt)
        elif state == "game_over":
            game_over_screen.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    from core.player_data import PlayerData
    player_data = PlayerData()
    main(player_data)
