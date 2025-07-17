import pygame
import sys

from core.room_manager import RoomManager
from core.player import Player
from inventory.grid_inventory import GridInventory
from inventory.item import Item
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TILE_SIZE


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Your Game Title")
    clock = pygame.time.Clock()

    room_manager = RoomManager()
    current_room = room_manager.get_current_room()
    player = Player(100, 100)

    inventory = GridInventory(columns=5, rows=4)
    inventory_visible = False

    test_item = Item("sword", width=1, height=2)
    inventory.place_item(test_item, 0, 0)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_i:
                    inventory_visible = not inventory_visible

            if inventory_visible:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        inventory.start_drag(pygame.mouse.get_pos(), TILE_SIZE)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        inventory.drop_drag(pygame.mouse.get_pos(), TILE_SIZE)

        screen.fill((20, 20, 20))

        if inventory_visible:
            for item, x, y in inventory.items:
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, item.width * TILE_SIZE, item.height * TILE_SIZE)
                pygame.draw.rect(screen, (200, 200, 200), rect)
                pygame.draw.rect(screen, (100, 100, 100), rect, 2)

            if inventory.dragged_item:
                mx, my = pygame.mouse.get_pos()
                dx, dy = inventory.drag_offset
                draw_x = mx - dx * TILE_SIZE
                draw_y = my - dy * TILE_SIZE
                rect = pygame.Rect(draw_x, draw_y,
                                   inventory.dragged_item.width * TILE_SIZE,
                                   inventory.dragged_item.height * TILE_SIZE)
                pygame.draw.rect(screen, (180, 180, 0), rect)
                pygame.draw.rect(screen, (255, 255, 0), rect, 2)

        else:
            for wall in current_room.walls:
                pygame.draw.rect(screen, (100, 100, 100), wall)

            for npc in current_room.npcs:
                npc.draw(screen)

            for enemy in current_room.enemies:
                enemy.draw(screen)

            player.update(dt, current_room.walls)
            player.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

