def check_collision(a, b):
    return a.rect.colliderect(b.rect)

def handle_room_transition(player, room_manager, width, height):
    new_coords = list(room_manager.current_coords)
    if player.rect.right > width:
        new_coords[0] += 1
        player.rect.left = 0
    elif player.rect.left < 0:
        new_coords[0] -= 1
        player.rect.right = width
    elif player.rect.top < 0:
        new_coords[1] -= 1
        player.rect.bottom = height
    elif player.rect.bottom > height:
        new_coords[1] += 1
        player.rect.top = 0
    else:
        return

    new_coords = tuple(new_coords)
    if new_coords in room_manager.rooms:
        room_manager.current_coords = new_coords
    else:
        print("placeholder, exit game")
        pygame.quit()
        sys.exit()
      
def handle_inventory():
  pass
